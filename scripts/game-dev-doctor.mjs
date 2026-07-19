import {execFileSync} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const root=process.cwd(),json=process.argv.includes('--json'),checks=[];
const add=(name,status,detail)=>checks.push({name,status,detail});
const command=(file,args=[])=>{try{return execFileSync(file,args,{encoding:'utf8',stdio:['ignore','pipe','pipe']}).trim()}catch{return null}};
const nodeMajor=Number(process.versions.node.split('.')[0]);add('Node.js',nodeMajor>=22?'pass':'fail',process.version+' (22+ required)');
const pnpmFromEnv=(process.env.npm_config_user_agent||'').match(/pnpm\/([^\s]+)/)?.[1];const pnpm=pnpmFromEnv||command('pnpm',['--version'])||command('corepack',['pnpm','--version']);add('pnpm',pnpm?'pass':'fail',pnpm||'not found');
const python=command(process.platform==='win32'?'python.exe':'python',['--version']);add('Python',python?'pass':'fail',python||'not found');
const git=command('git',['--version']);add('Git',git?'pass':'fail',git||'not found');
for(const file of ['package.json','pnpm-lock.yaml','.node-version','.python-version','tsconfig.json','wrangler.jsonc','data/release-manifest.json','scripts/build_level_viewer_v4.py','tests/game_core.test.ts','tests/e2e_startup_performance.py','.githooks/pre-commit','.githooks/pre-push','.github/workflows/game-quality.yml'])add(file,fs.existsSync(path.join(root,file))?'pass':'fail',fs.existsSync(path.join(root,file))?'present':'missing');
let badJson=0;for(const dir of ['data','packages/assets'])for(const file of fs.readdirSync(path.join(root,dir),{recursive:true}).filter(x=>String(x).endsWith('.json'))){try{JSON.parse(fs.readFileSync(path.join(root,dir,String(file)),'utf8'))}catch{badJson++}}add('JSON content',badJson?'fail':'pass',badJson?`${badJson} invalid files`:'all parse');
const source=path.join(root,'scripts/build_level_viewer_v4.py'),generated=path.join(root,'apps/wecr8-info/prototypes/shop-floor-viewer.html');add('Generated game',!fs.existsSync(generated)?'warn':fs.statSync(generated).mtimeMs>=fs.statSync(source).mtimeMs?'pass':'warn',!fs.existsSync(generated)?'missing; run pnpm game:generate':fs.statSync(generated).mtimeMs>=fs.statSync(source).mtimeMs?'current':'stale; run pnpm game:generate');
const status=command('git',['status','--porcelain']);add('Git worktree',status?'warn':'pass',status?'local changes present':'clean');
const result={ok:!checks.some(x=>x.status==='fail'),generatedAt:new Date().toISOString(),checks};
if(json)console.log(JSON.stringify(result,null,2));else{console.log('\nREINDUSTRIALIZE GAME DEV DOCTOR\n');for(const c of checks)console.log(`${c.status==='pass'?'[x]':c.status==='warn'?'[!]':'[ ]'} ${c.name}: ${c.detail}`);console.log(`\n${result.ok?'READY':'NOT READY'} · ${checks.filter(x=>x.status==='pass').length}/${checks.length} checks passed`)}
if(!result.ok)process.exit(1);
