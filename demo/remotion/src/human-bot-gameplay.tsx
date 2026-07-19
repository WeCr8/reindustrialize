import React from 'react';
import {AbsoluteFill,Audio,OffthreadVideo,Sequence,interpolate,staticFile,useCurrentFrame,useVideoConfig} from 'remotion';
import bot from '../../../data/human-bot-gameplay-video.json';
import timing from '../../../data/promo-voiceover-timing.json';

export const HumanBotFullGameplayV5:React.FC=()=>{const {durationInFrames}=useVideoConfig();return <AbsoluteFill style={{background:'#05070a'}}>
 <OffthreadVideo src={staticFile(bot.source)} style={{width:'100%',height:'100%',objectFit:'contain'}}/>
 <Audio loop src={staticFile('audio/garage_shift.mp3')} volume={(f)=>interpolate(f,[0,45,durationInFrames-45,durationInFrames-1],[0,.12,.12,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}/>
 <div style={{position:'absolute',top:26,right:34,color:'#3fd08a',fontFamily:'Arial Black,Arial',fontSize:17,letterSpacing:2,textShadow:'3px 3px #000'}}>HUMAN-STYLE BOT PLAYTEST · SEED {bot.seed}</div>
 </AbsoluteFill>};

export const botHorizontal60=[
 {from:0,duration:420,label:'MEET ZACH AND CREATE YOUR FOUNDER'},
 {from:900,duration:420,label:'TOUR THE GARAGE SHOP'},
 {from:2250,duration:540,label:'ORDER MATERIAL AND START PRODUCTION'},
 {from:4860,duration:420,label:'COMPLETE FIVE JOBS AND EXPAND'},
];
export const botFeature45=[
 {from:2100,duration:360,label:'ORDER CERTIFIED RAW STOCK'},
 {from:2700,duration:540,label:'CUT STOCK · SET TOOLS · PROVE G-CODE'},
 {from:4500,duration:450,label:'RUN CNC · INSPECT · GROW'},
];
export const botSocial30=[
 {from:150,duration:270,label:'BUILD YOUR FOUNDER'},
 {from:2460,duration:360,label:'LEARN BY DOING'},
 {from:5070,duration:270,label:'OUTGROW THE GARAGE'},
];

export const heroV6Segments=[
 {from:0,duration:270,label:'CREATE YOUR FOUNDER AND COMPANY',playbackRate:1},
 {from:450,duration:270,label:'MOVE THROUGH THE GARAGE SHOP',playbackRate:1},
 {from:750,duration:270,label:'CUT STOCK · SET TOOLS · PROVE G-CODE',playbackRate:1},
 {from:1050,duration:270,label:'RUN THE CNC AND VERIFY THE RESULT',playbackRate:1},
 {from:4110,duration:270,label:'COMPLETE THE PART · EARN AN A GRADE',playbackRate:.6667},
];

const voiceovers=timing.voiceovers as Record<string,{role?:string;durationFrames:number;transcript:string;segments:{from:number;to:number;text:string}[]}>;
const Caption:React.FC<{voice:string}>=({voice})=>{const frame=useCurrentFrame();const item=voiceovers[voice];const player=item.role==='player';const accent=player?'#45c7f4':'#e8b93b';const segment=item.segments.find(x=>frame>=x.from&&frame<x.to);return <div style={{position:'absolute',zIndex:20,left:'6%',right:'6%',bottom:'7%',background:'rgba(5,8,12,.96)',border:`4px solid ${accent}`,boxShadow:'8px 8px #000',padding:'18px 22px',fontFamily:'Arial'}}><div style={{color:accent,fontWeight:900,fontSize:22,letterSpacing:3}}>{player?'PLAYER PERSPECTIVE · SCRIPTED PROMO':'ZACH · SHOP TEACHER & BUSINESS MENTOR'}</div><div style={{color:'#fff',fontWeight:800,fontSize:36,lineHeight:1.2,marginTop:8}}>{segment?.text||item.transcript}</div></div>};
const HeroLabel:React.FC<{label:string}>=({label})=>{const frame=useCurrentFrame();const opacity=interpolate(frame,[0,10,210,260],[0,1,1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});return <><div style={{position:'absolute',top:30,right:36,color:'#3fd08a',fontFamily:'Arial Black,Arial',fontSize:18,letterSpacing:3,textShadow:'3px 3px #000'}}>REAL BOT-RECORDED GAMEPLAY · V6</div><div style={{position:'absolute',opacity,left:36,bottom:34,maxWidth:1040,background:'rgba(5,8,12,.94)',border:'4px solid #e8b93b',boxShadow:'7px 7px #000',padding:'13px 19px',color:'#fff',fontFamily:'Arial Black,Arial',fontSize:30}}>{label}</div></>};

export const HeroGameplayDemoV6:React.FC=()=>{const {durationInFrames}=useVideoConfig();let cursor=0;const player=voiceovers.player_review_gameplay;const zach=voiceovers.zach_welcome;const playerStart=585,zachStart=45;return <AbsoluteFill style={{background:'#05070a',overflow:'hidden'}}>
 <Audio loop src={staticFile('audio/garage_shift.mp3')} volume={(f)=>{const base=interpolate(f,[0,30,durationInFrames-30,durationInFrames-1],[0,.22,.22,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});const speaking=(f>=playerStart&&f<playerStart+player.durationFrames)||(f>=zachStart&&f<zachStart+zach.durationFrames);return speaking?base*.28:base;}}/>
 <Sequence from={playerStart} durationInFrames={player.durationFrames}><Audio src={staticFile('audio/player_review_gameplay.mp3')} volume={.96}/><Caption voice="player_review_gameplay"/></Sequence>
 <Sequence from={zachStart} durationInFrames={zach.durationFrames}><Audio src={staticFile('audio/zach_welcome.mp3')} volume={.96}/><Caption voice="zach_welcome"/></Sequence>
 {heroV6Segments.map((segment,index)=>{const start=cursor;cursor+=segment.duration;return <Sequence key={`${segment.from}-${index}`} from={start} durationInFrames={segment.duration}><AbsoluteFill><OffthreadVideo muted playbackRate={segment.playbackRate} startFrom={segment.from} src={staticFile(bot.source)} style={{width:'100%',height:'100%',objectFit:'cover'}}/><HeroLabel label={segment.label}/></AbsoluteFill></Sequence>})}
 </AbsoluteFill>};

const campaignV7Segments=[
 {from:0,duration:240,label:'FOUND YOUR COMPANY'},
 {from:450,duration:240,label:'MOVE WITH PURPOSE'},
 {from:2100,duration:240,label:'WIN THE WORK · SOURCE THE STOCK'},
 {from:2700,duration:240,label:'CUT · TOOL · PROVE THE CODE'},
 {from:3300,duration:240,label:'RUN THE PROCESS'},
 {from:4110,duration:240,label:'INSPECT · DELIVER · GROW'},
];
const campaignV7Captions=[
 {from:45,to:190,text:'American manufacturing is moving again.'},
 {from:190,to:350,text:'In REINDUSTRIALIZE, you do not watch from the sidelines. You build the company.'},
 {from:350,to:520,text:'Start in an empty garage. Choose your founder. Learn from Zach.'},
 {from:520,to:690,text:'Win the work, order certified material, and cut stock.'},
 {from:690,to:850,text:'Set tools, read real G and M code, and inspect the first article.'},
 {from:850,to:1040,text:'Then hire the team, expand the floor, and turn one reliable job into a manufacturing powerhouse.'},
 {from:1040,to:1215,text:'This is where builders learn how production really works—'},
 {from:1215,to:1360,text:'one decision, one part, and one promise kept at a time.'},
 {from:1360,to:1440,text:'Your first shift starts now.'},
];
const CampaignCaption:React.FC=()=>{const frame=useCurrentFrame();const cue=campaignV7Captions.find(x=>frame>=x.from&&frame<x.to);if(!cue)return null;return <div style={{position:'absolute',left:'7%',right:'7%',bottom:'8%',display:'flex',justifyContent:'center'}}><div style={{maxWidth:1420,padding:'14px 22px',background:'rgba(3,8,12,.88)',borderLeft:'6px solid #f4bf35',color:'#fff',font:'800 34px/1.22 Arial',textAlign:'center',textShadow:'2px 2px #000',boxShadow:'0 12px 45px #000b'}}>{cue.text}</div></div>};
export const HeroCampaignV7:React.FC=()=>{const {durationInFrames}=useVideoConfig();const frame=useCurrentFrame();let cursor=0;return <AbsoluteFill style={{background:'#02070b',overflow:'hidden'}}>
 <Audio loop src={staticFile('audio/garage_shift.mp3')} volume={(f)=>interpolate(f,[0,30,durationInFrames-30,durationInFrames-1],[0,.055,.055,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}/>
 <Sequence from={30} durationInFrames={1310}><Audio src={staticFile('audio/hero_campaign_v7.mp3')} volume={1}/></Sequence>
 {campaignV7Segments.map((segment,index)=>{const start=cursor;cursor+=segment.duration;return <Sequence key={segment.from} from={start} durationInFrames={segment.duration}><AbsoluteFill><OffthreadVideo muted startFrom={segment.from} src={staticFile(bot.source)} style={{width:'100%',height:'100%',objectFit:'cover',transform:'scale(1.035)',filter:'contrast(1.08) saturate(.92) brightness(.82)'}}/><div style={{position:'absolute',inset:0,background:'linear-gradient(90deg,rgba(2,7,11,.72),transparent 46%,rgba(2,7,11,.24)),radial-gradient(circle at 50% 44%,transparent 45%,rgba(0,0,0,.55) 100%)'}}/><div style={{position:'absolute',top:36,left:48,color:'#f4bf35',font:'900 21px Arial Black',letterSpacing:5}}>REINDUSTRIALIZE</div><div style={{position:'absolute',top:38,right:48,color:'#e9f0f4',font:'800 15px monospace',letterSpacing:2}}>REAL GAMEPLAY · BUILD 0.7</div><div style={{position:'absolute',left:48,top:'20%',maxWidth:690,color:'#fff'}}><div style={{color:'#40df91',font:'900 18px monospace',letterSpacing:3}}>0{index+1} / 06</div><div style={{marginTop:12,font:'900 54px/.98 Arial Black',textTransform:'uppercase',textShadow:'4px 4px #000'}}>{segment.label}</div></div></AbsoluteFill></Sequence>})}
 <CampaignCaption/>
 <div style={{position:'absolute',left:0,bottom:0,height:6,width:`${(frame/(durationInFrames-1))*100}%`,background:'#f4bf35',boxShadow:'0 0 18px #f4bf35'}}/>
 </AbsoluteFill>};
