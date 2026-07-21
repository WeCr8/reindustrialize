(() => {
  'use strict';
  if (window.__reindAnalyticsInstalled) return;
  window.__reindAnalyticsInstalled = true;
  const STORAGE_KEY = 'reindustrialize.analyticsConsent.v1';
  const SESSION_KEY = 'reindustrialize.analyticsEvents.v1';
  const ALLOWED = {
    landing_play: [], hero_video_play: [], hero_video_complete: [],
    game_start: [], game_resume: [], founder_select: ['archetype'], control_mode: ['mode'],
    station_start: ['station_id'], task_complete: ['task_id', 'station_id'],
    hire_role: ['role_id'], worker_assignment: ['station_id', 'skill_fit'],
    equipment_purchase: ['equipment_id', 'tier'], maintenance_repair: ['equipment_id'],
    chapter_milestone: ['chapter'], facility_milestone: ['facility_id']
  };
  const FORBIDDEN = /name|company|factory|save|text|input|email|phone|voice|message/i;
  const ONCE_PER_SESSION = new Set(['landing_play', 'hero_video_play', 'hero_video_complete', 'game_start', 'game_resume']);
  const PERSISTENT = new Set(['chapter_milestone', 'facility_milestone']);
  const recent = new Map();
  let pageViewSent = false;
  const safeValue = value => typeof value === 'number' ? Number.isFinite(value) && value >= 0 && value <= 1000 :
    typeof value === 'string' && /^[a-z0-9][a-z0-9_-]{0,47}$/i.test(value);
  const readChoice = () => { try { return localStorage.getItem(STORAGE_KEY); } catch { return null; } };
  const readSessionEvents = () => { try { return new Set(JSON.parse(sessionStorage.getItem(SESSION_KEY) || '[]')); } catch { return new Set(); } };
  const sessionEvents = readSessionEvents();
  const rememberSessionEvent = key => { sessionEvents.add(key); try { sessionStorage.setItem(SESSION_KEY, JSON.stringify([...sessionEvents])); } catch {} };
  const persistentKey = key => `reindustrialize.analyticsOnce.v1.${key}`;
  const sendPageView = () => {
    if (pageViewSent || readChoice() !== 'accepted' || typeof window.gtag !== 'function') return;
    pageViewSent = true;
    window.gtag('event', 'page_view', {page_location: location.origin + location.pathname, page_title: document.title});
  };
  const updateConsent = choice => {
    if (typeof window.gtag !== 'function') return;
    const granted = choice === 'accepted' ? 'granted' : 'denied';
    window.gtag('consent', 'update', {
      analytics_storage: granted,
      ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'
    });
    if (choice === 'accepted') sendPageView();
  };
  const stored = readChoice();
  if (stored === 'accepted' || stored === 'declined') updateConsent(stored);
  window.reindAnalytics = (eventName, params = {}) => {
    if (readChoice() !== 'accepted' || !Object.hasOwn(ALLOWED, eventName)) return false;
    const clean = {};
    for (const key of ALLOWED[eventName]) {
      if (!FORBIDDEN.test(key) && Object.hasOwn(params, key) && safeValue(params[key])) clean[key] = params[key];
    }
    const signature = `${eventName}:${JSON.stringify(clean)}`;
    const now = Date.now();
    if ((recent.get(signature) || 0) > now - 2500) return false;
    if (ONCE_PER_SESSION.has(eventName) && sessionEvents.has(eventName)) return false;
    if (PERSISTENT.has(eventName)) {
      try { if (localStorage.getItem(persistentKey(signature))) return false; } catch {}
    }
    window.gtag?.('event', eventName, clean);
    recent.set(signature, now);
    if (ONCE_PER_SESSION.has(eventName)) rememberSessionEvent(eventName);
    if (PERSISTENT.has(eventName)) { try { localStorage.setItem(persistentKey(signature), 'sent'); } catch {} }
    (window.__reindAnalyticsDebug ||= []).push({event:eventName, params:clean, at:now});
    return true;
  };
  window.addEventListener('reind:analytics', event => {
    const detail = event.detail || {};
    window.reindAnalytics(detail.event, detail.params || {});
  });

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
  function instrument() {
    document.addEventListener('click', e => {
      const el = e.target.closest('button,a'); if (!el) return;
      if (el.closest('a[href="/game/"],a[href="/play"]')) window.reindAnalytics('landing_play');
      if (el.matches('#soundBeacon,#heroSound,.card[data-src]')) window.reindAnalytics('hero_video_play');
    });
    document.querySelectorAll('video').forEach(video => video.addEventListener('ended',()=>window.reindAnalytics('hero_video_complete')));
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded',()=>{showBanner();instrument();}); else {showBanner();instrument();}
})();
