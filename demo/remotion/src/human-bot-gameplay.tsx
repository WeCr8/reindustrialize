import React from 'react';
import {AbsoluteFill,Audio,OffthreadVideo,interpolate,staticFile,useVideoConfig} from 'remotion';
import bot from '../../../data/human-bot-gameplay-video.json';

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
