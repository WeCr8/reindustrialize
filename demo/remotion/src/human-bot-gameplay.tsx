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
