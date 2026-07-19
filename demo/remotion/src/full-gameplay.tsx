import React from 'react';
import {AbsoluteFill,Audio,OffthreadVideo,Sequence,interpolate,staticFile,useCurrentFrame,useVideoConfig} from 'remotion';
import metadata from '../../../data/full-gameplay-video.json';

const IntroLabel:React.FC=()=>{const frame=useCurrentFrame();const opacity=interpolate(frame,[0,12,120,150],[0,1,1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});return <div style={{position:'absolute',opacity,left:54,top:42,background:'rgba(5,8,12,.94)',border:'4px solid #e8b93b',boxShadow:'7px 7px 0 #000',padding:'15px 22px',fontFamily:'Arial, sans-serif'}}><div style={{color:'#e8b93b',fontSize:24,fontWeight:900,letterSpacing:3}}>FULL CURRENT GAMEPLAY · V3</div><div style={{color:'#fff',fontSize:32,fontWeight:900,marginTop:4}}>GARAGE BAY → JOB SHOP EXPANSION</div></div>};

export const FullGameplayV3:React.FC=()=>{const {durationInFrames}=useVideoConfig();return <AbsoluteFill style={{background:'#05070a'}}><OffthreadVideo src={staticFile(metadata.source)} style={{width:'100%',height:'100%',objectFit:'contain'}}/><Audio loop src={staticFile('audio/garage_shift.mp3')} volume={(f)=>interpolate(f,[0,45,durationInFrames-60,durationInFrames-1],[0,.2,.2,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}/><Sequence from={0} durationInFrames={160}><IntroLabel/></Sequence></AbsoluteFill>};
