(() => {
  'use strict';
  const STORAGE_KEY = 'reindustrialize.analyticsConsent.v1';
  const ALLOWED = {
    landing_play: [], hero_video_play: [], hero_video_complete: [],
    game_start: [], game_resume: [], founder_select: ['archetype'], control_mode: ['mode'],
    station_start: ['station_id'], task_complete: ['task_id', 'station_id'],
    hire_role: ['role_id'], worker_assignment: ['station_id', 'skill_fit'],
    equipment_purchase: ['equipment_id', 'tier'], maintenance_repair: ['equipment_id'],
    chapter_milestone: ['chapter'], facility_milestone: ['facility_id']
  };
  const FORBIDDEN = /name|company|factory|save|text|input|email|phone|voice|message/i;
  const safeValue = value => typeof value === 'number' ? Number.isFinite(value) && value >= 0 && value <= 1000 :
    typeof value === 'string' && /^[a-z0-9][a-z0-9_-]{0,47}$/i.test(value);
  const readChoice = () => { try { return localStorage.getItem(STORAGE_KEY); } catch { return null; } };
  const updateConsent = choice => {
    if (typeof window.gtag !== 'function') return;
    const granted = choice === 'accepted' ? 'granted' : 'denied';
    window.gtag('consent', 'update', {
      analytics_storage: granted,
      ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'
    });
  };
  const stored = readChoice();
  if (stored === 'accepted' || stored === 'declined') updateConsent(stored);
  window.reindAnalytics = (eventName, params = {}) => {
    if (readChoice() !== 'accepted' || !Object.hasOwn(ALLOWED, eventName)) return false;
    const clean = {};
    for (const key of ALLOWED[eventName]) {
      if (!FORBIDDEN.test(key) && Object.hasOwn(params, key) && safeValue(params[key])) clean[key] = params[key];
    }
    window.gtag?.('event', eventName, clean);
    return true;
  };

  function choose(choice) {
    try { localStorage.setItem(STORAGE_KEY, choice); } catch {}
    updateConsent(choice);
    document.getElementById('privacyConsent')?.remove();
  }
  function showBanner() {
    if (readChoice() || document.getElementById('privacyConsent')) return;
    const root = document.createElement('section');
    root.id = 'privacyConsent';
    root.setAttribute('role', 'dialog');
    root.setAttribute('aria-label', 'Analytics privacy choice');
    root.innerHTML = '<div><strong>YOUR PRIVACY, YOUR CHOICE</strong><p>Optional analytics help us improve anonymous game progress and performance. We never send founder or factory names, save data, free text, or raw controls.</p></div><div class="privacyActions"><button type="button" data-consent="declined">DECLINE</button><button type="button" data-consent="accepted">ACCEPT ANALYTICS</button></div>';
    const style = document.createElement('style');
    style.textContent = '#privacyConsent{position:fixed;z-index:2147483647;left:12px;right:12px;bottom:12px;display:flex;align-items:center;justify-content:space-between;gap:16px;max-width:980px;margin:auto;padding:14px 16px;background:#08131cee;color:#fff;border:2px solid #53d68b;box-shadow:0 8px 35px #000b;font:16px/1.35 system-ui,sans-serif}#privacyConsent strong{color:#e8b93b}#privacyConsent p{margin:5px 0 0;max-width:680px}.privacyActions{display:flex;gap:8px;flex:none}.privacyActions button{min-height:42px;padding:8px 13px;background:#122431;color:#fff;border:2px solid #8ba1ad;font-weight:800}.privacyActions button[data-consent=accepted]{background:#1b6b48;border-color:#53d68b}@media(max-width:700px){#privacyConsent{display:block}.privacyActions{margin-top:10px}.privacyActions button{flex:1}}';
    document.head.append(style); document.body.append(root);
    root.addEventListener('click', e => { const choice = e.target?.dataset?.consent; if (choice) choose(choice); });
  }
  const slug = value => String(value || '').toLowerCase().replace(/[^a-z0-9_-]/g, '_').slice(0, 48);
  const roleMap = new Map([
    ['CNC Operator', 'cnc_operator'], ['CNC Programmer', 'cnc_programmer'],
    ['Quality Inspector', 'quality_inspector'], ['Maintenance Technician', 'maintenance_technician'],
    ['Material Handler', 'material_handler'], ['Setup Technician', 'setup_technician']
  ]);
  const equipmentTier = id => ({saw:1, vmc:1, inspection:1, tig_manual:2, surface_grinder:2, cnc_lathe:2, polymer_print_farm:2, starter_tugger_agv:2, five_axis_vmc:3, robotic_tig:3, amr_wip_fleet:3, metal_additive:4, cmm:4, heavy_mobile_robot_platform:4, xray:5, cobot:5, humanoid_factory_assistant:6}[id] || 1);
  function instrument() {
    document.addEventListener('click', e => {
      const el = e.target.closest('button,a,[data-avatar],[data-control]'); if (!el) return;
      if (el.id === 'newGame') window.reindAnalytics('game_start');
      if (el.id === 'continueGame') window.reindAnalytics('game_resume');
      if (el.matches('.avatarChoice[data-avatar]')) window.reindAnalytics('founder_select', {archetype: slug(el.dataset.avatar)});
      if (el.matches('.controlChoice[data-control]')) window.reindAnalytics('control_mode', {mode: slug(el.dataset.control)});
      if (el.id === 'objectiveAction' || el.id === 'stationOpen') window.reindAnalytics('station_start', {station_id:'current_objective'});
      const tasks = {cutStock:['stock_cut','saw'], installKit:['tool_setup','tool_crib'], cycst:['cnc_cycle','vmc'], tdone:['inspection','inspection'], repairVmc:['vmc_repair','vmc']};
      if (tasks[el.id]) window.reindAnalytics(el.id === 'repairVmc' ? 'maintenance_repair' : 'task_complete', el.id === 'repairVmc' ? {equipment_id:'vmc'} : {task_id:tasks[el.id][0], station_id:tasks[el.id][1]});
      if (el.matches('.noxOrder')) window.reindAnalytics('task_complete', {task_id:'material_order', station_id:'jobline'});
      if (el.matches('[data-buy-equipment]')) { const id=slug(el.dataset.buyEquipment); window.reindAnalytics('equipment_purchase',{equipment_id:id,tier:equipmentTier(id)}); }
      if (el.id === 'hireNow' || el.id === 'profileHire') { const label=document.querySelector('.hireCard .role, #profile .role')?.textContent?.split('·')[0]?.trim(); window.reindAnalytics('hire_role',{role_id:roleMap.get(label)||'factory_team'}); }
      if (el.id === 'b1') window.reindAnalytics('facility_milestone',{facility_id:'garage_bay'});
      if (el.id === 'b2') window.reindAnalytics('facility_milestone',{facility_id:'job_shop'});
      if (el.closest('a[href="/game/"],a[href="/play"]')) window.reindAnalytics('landing_play');
    }, true);
    document.addEventListener('change', e => { if (e.target.matches('.assignSelect')) window.reindAnalytics('worker_assignment',{station_id:slug(e.target.value || 'unassigned'),skill_fit:'qualified'}); }, true);
    document.querySelectorAll('video').forEach(video => { video.addEventListener('play',()=>window.reindAnalytics('hero_video_play'),{once:true}); video.addEventListener('ended',()=>window.reindAnalytics('hero_video_complete'),{once:true}); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded',()=>{showBanner();instrument();}); else {showBanner();instrument();}
})();
