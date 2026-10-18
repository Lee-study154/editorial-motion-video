import React from 'react';
import {AbsoluteFill, Audio, Composition, Img, Sequence, interpolate, registerRoot,
  staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import project from '../project.json';

type Shot = {id: string; kind: string; seconds: number; title: string; subtitle?: string;
  asset?: string; source?: string; motion: string};
type Track = {asset: string; start?: number; volume: number};
type Project = {name: string; width: number; height: number; fps: number;
  color: {paper: string; ink: string; accent: string}; illustrationMax: number;
  lead: string; shots: Shot[]; audio: Track[]};
const local = (asset: string) => /^https?:/.test(asset) ? asset : staticFile(asset);
const ShotView = ({shot, config}: {shot: Shot; config: Project}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const p = interpolate(t, [0, .55], [0, 1], {extrapolateRight: 'clamp'});
  const drift = interpolate(t, [0, shot.seconds], [0, 1], {extrapolateRight: 'clamp'});
  const isPage = shot.kind === 'page';
  const camera = shot.motion === 'page-tilt' ?
    `perspective(1800px) rotateY(${(-12 + p * 9)}deg) rotateX(${8 - p * 6}deg) scale(${.86 + p * .1 + drift * .04})` :
    shot.motion === 'character-float' ? `translateY(${Math.sin(t * 2) * 8}px) scale(${.93 + p * .07})` :
    `translateY(${(1-p)*32}px) scale(${.9 + p*.1})`;
  return <AbsoluteFill style={{background: config.color.paper, color: config.color.ink,
    fontFamily: 'Arial, sans-serif', padding: '7%', justifyContent: 'center', overflow: 'hidden'}}>
    <div style={{fontSize: 22, letterSpacing: 3, color: config.color.accent,
      marginBottom: 28}}>{config.name.toUpperCase()}</div>
    <div style={{fontSize: isPage ? 62 : 98, fontWeight: 700, lineHeight: 1.05,
      letterSpacing: -3, opacity: p, marginBottom: 22}}>{shot.title}</div>
    {shot.subtitle && <div style={{fontSize: 30, lineHeight: 1.4, opacity: p * .7,
      maxWidth: '85%', marginBottom: 36}}>{shot.subtitle}</div>}
    {shot.asset && <div style={{width: isPage ? '100%' : '72%', alignSelf: 'center',
      transform: camera, transformOrigin: 'center', opacity: p, borderRadius: isPage ? 18 : 0,
      overflow: 'hidden', boxShadow: isPage ? '0 25px 75px #13213f20' : undefined}}>
      <Img src={local(shot.asset)} style={{display: 'block', width: '100%', maxHeight: config.height * .56, objectFit: 'contain'}} />
    </div>}
    <div style={{position: 'absolute', bottom: '4%', fontSize: 18, opacity: .45}}>{shot.id}</div>
  </AbsoluteFill>;
};
export const Film = (config: Project) => {
  let offset = 0;
  return <AbsoluteFill>{config.shots.map(shot => {
    const from = offset;
    const durationInFrames = Math.round(shot.seconds * config.fps);
    offset += durationInFrames;
    return <Sequence key={shot.id} from={from} durationInFrames={durationInFrames}>
      <ShotView shot={shot} config={config}/>
    </Sequence>;
  })}{config.audio.map((track, i) => <Sequence key={i} from={Math.round((track.start || 0)*config.fps)}>
    <Audio src={local(track.asset)} volume={track.volume}/>
  </Sequence>)}</AbsoluteFill>;
};
const Root = () => <Composition id="EditorialFilm" component={Film}
  width={project.width} height={project.height} fps={project.fps}
  durationInFrames={Math.round(project.shots.reduce((n,s)=>n+s.seconds,0)*project.fps)}
  defaultProps={project} calculateMetadata={({props})=>({width: props.width,
    height: props.height, fps: props.fps,
    durationInFrames: props.shots.reduce((n,s)=>n+Math.round(s.seconds*props.fps),0)})}/>;
registerRoot(Root);
