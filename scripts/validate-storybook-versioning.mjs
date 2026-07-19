import fs from 'node:fs';import path from 'node:path';
const root=process.cwd(),release=JSON.parse(fs.readFileSync(path.join(root,'data/release-manifest.json'),'utf8')),registry=JSON.parse(fs.readFileSync(path.join(root,'storybook/releases.json'),'utf8')),fail=[];
if(!release.storybookRequired)fail.push('release manifest must require a storybook');
const edition=registry.editions.find(e=>e.edition===release.storybookEdition&&e.gameRelease===release.release);
if(!edition)fail.push(`release ${release.release} has no registered ${release.storybookEdition} storybook`);
if(registry.currentEdition!==release.storybookEdition)fail.push('storybook registry current edition differs from release manifest');
if(edition){for(const key of ['manifest','viewer','slides'])if(!fs.existsSync(path.join(root,'storybook',edition[key])))fail.push(`registered ${key} is missing: ${edition[key]}`);const m=JSON.parse(fs.readFileSync(path.join(root,'storybook',edition.manifest),'utf8'));if(m.slideCount!==edition.slideCount)fail.push('registered slide count differs from edition manifest');if(m.gameBuild!==release.release)fail.push(`storybook gameBuild ${m.gameBuild} differs from release ${release.release}`)}
if(fail.length){console.error(fail.map(x=>'FAIL: '+x).join('\n'));process.exit(1)}console.log(`PASS: release ${release.release} is locked to storybook ${edition.edition} with ${edition.slideCount} slides.`);
