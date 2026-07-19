import React from 'react';
import {Composition} from 'remotion';
import {GameDemo,GameDemoV2} from './video';
import {Promo} from './promo';
import {FullGameplayV3} from './full-gameplay';
import fullGameplay from '../../../data/full-gameplay-video.json';
import {RealGameplayPromo,horizontal60,gameplay45,social30} from './real-gameplay-promo';
import {HeroGameplayDemoV6,HumanBotFullGameplayV5,botHorizontal60,botFeature45,botSocial30} from './human-bot-gameplay';
import humanBot from '../../../data/human-bot-gameplay-video.json';
export const RemotionRoot: React.FC = () => <>
 <Composition id="ReindustrializeDemo" component={GameDemo} durationInFrames={1800} fps={30} width={1920} height={1080}/>
 <Composition id="ReindustrializeVerticalShort" component={GameDemo} durationInFrames={1800} fps={30} width={1080} height={1920}/>
 <Composition id="ReindustrializeSquareSocial" component={GameDemo} durationInFrames={1800} fps={30} width={1080} height={1080}/>
 <Composition id="LaunchTrailer30" component={Promo} defaultProps={{indices:[0,2,3,7],music:'founding_dawn',voice:'zach_welcome'}} durationInFrames={900} fps={30} width={1920} height={1080}/>
 <Composition id="GameplayFeatureReel45" component={Promo} defaultProps={{indices:[3,4,5,6],music:'precision_run'}} durationInFrames={1350} fps={30} width={1920} height={1080}/>
 <Composition id="FounderSelectionShort20" component={Promo} defaultProps={{indices:[0,1,2],music:'garage_shift'}} durationInFrames={600} fps={30} width={1080} height={1920}/>
 <Composition id="ZachMentorPromo30" component={Promo} defaultProps={{indices:[2,3,5],music:'planning_office',voice:'zach_welcome'}} durationInFrames={900} fps={30} width={1080} height={1920}/>
 <Composition id="BusinessGrowthPromo30" component={Promo} defaultProps={{indices:[4,6,7],music:'factory_expansion',voice:'zach_expansion'}} durationInFrames={900} fps={30} width={1080} height={1080}/>
 <Composition id="PlayerReviewLaunch30" component={Promo} defaultProps={{indices:[0,2,3,7],music:'founding_dawn',voice:'player_review_launch'}} durationInFrames={900} fps={30} width={1920} height={1080}/>
 <Composition id="PlayerReviewGameplay30" component={Promo} defaultProps={{indices:[3,4,5,6],music:'precision_run',voice:'player_review_gameplay'}} durationInFrames={900} fps={30} width={1080} height={1920}/>
 <Composition id="PlayerReviewGrowth30" component={Promo} defaultProps={{indices:[4,6,7],music:'factory_expansion',voice:'player_review_growth'}} durationInFrames={900} fps={30} width={1080} height={1080}/>
 <Composition id="ReindustrializeDemoV2" component={GameDemoV2} durationInFrames={1800} fps={30} width={1920} height={1080}/>
 <Composition id="ReindustrializeVerticalShortV2" component={GameDemoV2} durationInFrames={1800} fps={30} width={1080} height={1920}/>
 <Composition id="ReindustrializeSquareSocialV2" component={GameDemoV2} durationInFrames={1800} fps={30} width={1080} height={1080}/>
 <Composition id="LaunchTrailer30V2" component={Promo} defaultProps={{version:2,indices:[0,2,3,8],music:'founding_dawn',voice:'zach_welcome'}} durationInFrames={900} fps={30} width={1920} height={1080}/>
 <Composition id="GameplayFeatureReel45V2" component={Promo} defaultProps={{version:2,indices:[3,4,5,6,7],music:'precision_run'}} durationInFrames={1350} fps={30} width={1920} height={1080}/>
 <Composition id="FounderSelectionShort20V2" component={Promo} defaultProps={{version:2,indices:[0,1,3],music:'garage_shift'}} durationInFrames={600} fps={30} width={1080} height={1920}/>
 <Composition id="ZachMentorPromo30V2" component={Promo} defaultProps={{version:2,indices:[2,3,4],music:'planning_office',voice:'zach_welcome'}} durationInFrames={900} fps={30} width={1080} height={1920}/>
 <Composition id="BusinessGrowthPromo30V2" component={Promo} defaultProps={{version:2,indices:[5,7,8],music:'factory_expansion',voice:'zach_expansion'}} durationInFrames={900} fps={30} width={1080} height={1080}/>
 <Composition id="PlayerReviewLaunch30V2" component={Promo} defaultProps={{version:2,indices:[0,2,3,8],music:'founding_dawn',voice:'player_review_launch'}} durationInFrames={900} fps={30} width={1920} height={1080}/>
 <Composition id="PlayerReviewGameplay30V2" component={Promo} defaultProps={{version:2,indices:[3,4,5,6],music:'precision_run',voice:'player_review_gameplay'}} durationInFrames={900} fps={30} width={1080} height={1920}/>
 <Composition id="PlayerReviewGrowth30V2" component={Promo} defaultProps={{version:2,indices:[5,7,8],music:'factory_expansion',voice:'player_review_growth'}} durationInFrames={900} fps={30} width={1080} height={1080}/>
 <Composition id="FullGameplayGarageToJobShopV3" component={FullGameplayV3} durationInFrames={fullGameplay.durationFrames} fps={30} width={1920} height={1080}/>
 <Composition id="RealGameplayDemoHorizontalV4" component={RealGameplayPromo} defaultProps={{segments:horizontal60,music:'garage_shift',edition:'HORIZONTAL V4'}} durationInFrames={1800} fps={30} width={1920} height={1080}/>
 <Composition id="RealGameplayFeature45V4" component={RealGameplayPromo} defaultProps={{segments:gameplay45,music:'precision_run',edition:'FEATURE V4'}} durationInFrames={1350} fps={30} width={1920} height={1080}/>
 <Composition id="RealGameplayVerticalShortV4" component={RealGameplayPromo} defaultProps={{segments:social30,music:'garage_shift',edition:'VERTICAL V4'}} durationInFrames={900} fps={30} width={1080} height={1920}/>
 <Composition id="RealGameplaySquareV4" component={RealGameplayPromo} defaultProps={{segments:social30,music:'factory_expansion',edition:'SQUARE V4'}} durationInFrames={900} fps={30} width={1080} height={1080}/>
 <Composition id="HumanBotFullGameplayV5" component={HumanBotFullGameplayV5} durationInFrames={humanBot.durationFrames} fps={30} width={1920} height={1080}/>
 <Composition id="HumanBotDemoHorizontalV5" component={RealGameplayPromo} defaultProps={{segments:botHorizontal60,music:'garage_shift',edition:'BOT PLAYTEST V5',source:humanBot.source}} durationInFrames={1800} fps={30} width={1920} height={1080}/>
 <Composition id="HumanBotFeature45V5" component={RealGameplayPromo} defaultProps={{segments:botFeature45,music:'precision_run',edition:'BOT FEATURE V5',source:humanBot.source}} durationInFrames={1350} fps={30} width={1920} height={1080}/>
 <Composition id="HumanBotVerticalShortV5" component={RealGameplayPromo} defaultProps={{segments:botSocial30,music:'garage_shift',edition:'BOT SHORT V5',source:humanBot.source}} durationInFrames={900} fps={30} width={1080} height={1920}/>
 <Composition id="HumanBotSquareV5" component={RealGameplayPromo} defaultProps={{segments:botSocial30,music:'factory_expansion',edition:'BOT SOCIAL V5',source:humanBot.source}} durationInFrames={900} fps={30} width={1080} height={1080}/>
 <Composition id="HeroGameplayDemoV6" component={HeroGameplayDemoV6} durationInFrames={1350} fps={30} width={1920} height={1080}/>
</>;
