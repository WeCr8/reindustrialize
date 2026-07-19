import React from 'react';
import {AbsoluteFill,Audio,Img,Sequence,interpolate,staticFile,useCurrentFrame,useVideoConfig} from 'remotion';
export const slides=[
['screens/01-title-and-company-creation.png','BUILD YOUR COMPANY','Start in a garage. Name the founder and the factory.'],
['screens/02-ten-founder-selection.png','CHOOSE YOUR FOUNDER','Ten selectable founders. One manufacturing ambition.'],
['screens/03-zach-founding-story.png','LEARN FROM ZACH','Practical mentorship turns every task into real shop knowledge.'],
['screens/04-playable-shop-objectives.png','RUN THE SHOP','Follow achievable objectives and operate the stations yourself.'],
['screens/05-nox-material-ordering.png','SOURCE REAL MATERIAL','Order certified stock and protect the cash that keeps the doors open.'],
['screens/06-cnc-equipment-view.png','MASTER THE MACHINES','Cut stock, set tools, read G-code, and prove the first article.'],
['screens/07-hire-your-team.png','BUILD THE TEAM','Review candidates, hire operators, and grow specialists into leaders.'],
['screens/08-factory-expansion.png','OUTGROW EVERY FACILITY','Expand from a borrowed garage into an American manufacturing powerhouse.'],
] as const;
export const slidesV2=[
['screens/v2/01-title-and-company-creation-v2.png','BUILD YOUR COMPANY','Create your founder, name the factory, and begin with one Garage Bay.'],
['screens/v2/02-ten-founder-selection-v2.png','CHOOSE YOUR FOUNDER','Ten selectable founders. Every one can walk, run, learn, and lead.'],
['screens/v2/03-zach-founding-story-v2.png','LEARN FROM ZACH','A real shop teacher and business mentor guides the company you control.'],
['screens/v2/04-founder-running-shop-floor-v2.png','MOVE WITH PURPOSE','Run the floor, follow the route, and reach the next production need fast.'],
['screens/v2/05-playable-shop-objectives-v2.png','USE EVERY STATION','Approach highlighted equipment and complete achievable manufacturing tasks.'],
['screens/v2/06-nox-material-ordering-v2.png','SOURCE REAL MATERIAL','Order certified stock and protect the cash that keeps the doors open.'],
['screens/v2/07-cnc-equipment-view-v2.png','MASTER THE MACHINES','Cut stock, set tools, read G-code, and prove the first article.'],
['screens/v2/08-hire-your-team-v2.png','BUILD THE TEAM','Review candidates, hire operators, and grow specialists into leaders.'],
['screens/v2/09-factory-expansion-v2.png','OUTGROW EVERY FACILITY','Expand from a garage into an American manufacturing powerhouse.'],
] as const;
export const Slide:React.FC<{src:string;title:string;copy:string;index:number;duration?:number}>=({src,title,copy,index,duration=225})=>{const frame=useCurrentFrame();const {width,height}=useVideoConfig();const portrait=height>width;const opacity=interpolate(frame,[0,15,duration-15,duration],[0,1,1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});const scale=interpolate(frame,[0,duration],[1.015,index%2?1.07:1.055]);const y=interpolate(frame,[0,duration],[index%2?-8:8,index%2?8:-8]);return <AbsoluteFill style={{opacity,background:'#05070a',overflow:'hidden'}}>{portrait&&<Img src={staticFile(src)} style={{width:'100%',height:'100%',objectFit:'cover',filter:'blur(28px) brightness(.35)',transform:'scale(1.12)'}}/>}<Img src={staticFile(src)} style={{width:'100%',height:'100%',objectFit:portrait?'contain':'cover',transform:`scale(${scale}) translateY(${y}px)`}}/><AbsoluteFill style={{background:'linear-gradient(180deg,transparent 38%,rgba(3,6,10,.35) 58%,rgba(3,6,10,.98) 100%)'}}/><div style={{position:'absolute',left:portrait?54:96,right:portrait?54:96,bottom:portrait?150:72,fontFamily:'Arial Black,Arial',textShadow:'4px 4px 0 #000'}}><div style={{color:'#e8b93b',fontSize:portrait?58:56,letterSpacing:2}}>{title}</div><div style={{color:'#f2f5f6',fontFamily:'Arial',fontWeight:700,fontSize:portrait?34:30,marginTop:10,maxWidth:1160}}>{copy}</div></div><div style={{position:'absolute',right:portrait?42:72,top:portrait?70:52,color:'#3fd08a',fontFamily:'monospace',fontWeight:900,fontSize:portrait?25:22,letterSpacing:3}}>REINDUSTRIALIZE</div></AbsoluteFill>};
export const GameDemo:React.FC=()=> <AbsoluteFill style={{background:'#05070a'}}><Audio src={staticFile('audio/founding_dawn.mp3')} volume={(f)=>interpolate(f,[0,45,1650,1799],[0,.32,.32,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}/>{slides.map(([src,title,copy],index)=><Sequence key={src} from={index*225} durationInFrames={225}><Slide src={src} title={title} copy={copy} index={index}/></Sequence>)}</AbsoluteFill>;
export const GameDemoV2:React.FC=()=> {const {durationInFrames}=useVideoConfig();const segment=Math.floor(durationInFrames/slidesV2.length);return <AbsoluteFill style={{background:'#05070a'}}><Audio src={staticFile('audio/garage_shift.mp3')} volume={(f)=>interpolate(f,[0,45,durationInFrames-45,durationInFrames-1],[0,.32,.32,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}/>{slidesV2.map(([src,title,copy],index)=><Sequence key={src} from={index*segment} durationInFrames={index===slidesV2.length-1?durationInFrames-index*segment:segment}><Slide src={src} title={title} copy={copy} index={index} duration={segment}/></Sequence>)}</AbsoluteFill>};
