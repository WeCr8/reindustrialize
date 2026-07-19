import {readFile,stat} from 'node:fs/promises';

const release=JSON.parse(await readFile('data/release-manifest.json','utf8'));
const luna=JSON.parse(await readFile('data/amazon-luna-release.json','utf8'));
const listing=JSON.parse(await readFile('release/amazon-luna/store-listing.json','utf8'));
const artifact=JSON.parse(await readFile('release/amazon-luna/artifact-manifest.json','utf8'));
const runtime=await readFile('scripts/build_level_viewer_v4.py','utf8');
const fail=[];
if(luna.preparedForGameRelease!==release.release)fail.push('Amazon bundle release differs from canonical release');
if(luna.submissionAttempted||luna.amazonApprovalClaimed)fail.push('bundle falsely claims Amazon submission or approval');
if(luna.bundleStatus!=='pre-authorization-draft'||luna.luna.status!=='intake-not-authorized')fail.push('authorization boundary status drifted');
if(luna.developerIdentityVerified||luna.authorizedAccountOwnerApproved)fail.push('identity or owner approval may not be inferred by repository preparation');
if(listing.status!=='draft-not-submitted')fail.push('store listing must remain an unsubmitted draft');
if(artifact.release!==release.release||artifact.storybookEdition!==release.storybookEdition||artifact.gameplayEvidenceVersion!==release.gameplayEvidenceVersion)fail.push('draft artifact identity differs from canonical release');
if(artifact.status!=='candidate-not-built'||artifact.sourceRevision||artifact.builtAtUtc||artifact.artifactFile||artifact.artifactSha256)fail.push('draft artifact manifest falsely claims an immutable platform build');
if(listing.longDescription.length>4000||/<[^>]+>/.test(listing.longDescription))fail.push('long description must be <=4000 characters and plain text');
if(listing.featureBullets.length<3||listing.featureBullets.length>5)fail.push('store listing requires 3–5 feature bullets');
if(!listing.longDescription.includes('Later facilities and campaign chapters remain in development'))fail.push('listing lacks honest later-chapter disclosure');
if(luna.appstoreAlternative.currentBinaryAvailable)fail.push('repository falsely claims an Appstore binary');
for(const family of ['Fire OS APK','Fire OS AAB','Vega OS VPKG'])if(!luna.appstoreAlternative.acceptedBinaryFamiliesFromOfficialDocs.includes(family))fail.push(`missing official Appstore binary family ${family}`);
for(const source of luna.officialSources){const host=new URL(source).hostname;if(!['developer.amazon.com','www.developer.amazon.com','amazonluna.blog'].includes(host))fail.push(`non-Amazon source in official register: ${source}`);}
for(const file of ['release/amazon-luna/test-instructions.md','release/amazon-luna/submission-checklist.md'])await stat(file);
if(!runtime.includes(luna.versionVisibility.currentTitleToken))fail.push('declared title version token is not present in the game generator');
if(!luna.versionVisibility.remainingImplementation.length)fail.push('version visibility gaps must remain explicit until implemented');
const serialized=JSON.stringify({luna,listing}).toLowerCase();for(const token of ['api_key','secret_key','password":"','access_token'])if(serialized.includes(token))fail.push(`credential-like field prohibited from release bundle: ${token}`);
if(fail.length){console.error(fail.map(x=>'FAIL: '+x).join('\n'));process.exit(1);}
console.log(`PASS: Amazon Luna/Appstore pre-authorization bundle matches ${release.release}, contains no submission claim or binary claim, and preserves authorized-owner boundaries.`);
