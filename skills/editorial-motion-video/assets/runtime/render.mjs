#!/usr/bin/env node
import {createRequire} from 'node:module';
import {existsSync} from 'node:fs';
import {mkdir, readFile} from 'node:fs/promises';
import path from 'node:path';
import {spawn} from 'node:child_process';
import {once} from 'node:events';
const args = process.argv.slice(2);
const value = (name, fallback) => args.includes(name) ? args[args.indexOf(name)+1] : fallback;
if (args.includes('--help')) {
  console.log('node render.mjs [--still --frame N] [--props project.json] [--scale 1] [--out path]');
  console.log('Optional --from N --to N render a video range. --browser /path/to/chrome selects a browser.');
  console.log('EDITORIAL_NODE_MODULES may point to an existing dependency directory; no install is automatic.');
  process.exit(0);
}
const browserPath = value('--browser', process.env.CHROME_PATH) || [
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser',
  process.env.ProgramFiles && path.join(process.env.ProgramFiles,'Google/Chrome/Application/chrome.exe')
].find(candidate => candidate && existsSync(candidate));
if (!browserPath || !existsSync(browserPath)) throw new Error('No existing Chrome found. Set CHROME_PATH or --browser to an installed browser; no download was attempted.');
const root = process.cwd();
const modules = process.env.EDITORIAL_NODE_MODULES;
const require = createRequire(modules ? path.join(modules, '../package.json') : path.join(root, 'package.json'));
const {bundle} = require('@remotion/bundler');
const {openBrowser, renderMedia, renderStill, selectComposition} = require('@remotion/renderer');
const manifest = JSON.parse(await readFile(path.join(root,'render-config.json'),'utf8'));
const inputProps = args.includes('--props') ? JSON.parse(await readFile(path.resolve(value('--props')),'utf8')) : {};
const output = path.resolve(value('--out',args.includes('--still')?'out/still.png':'out/film.mp4'));
await mkdir(path.dirname(output),{recursive:true});
const serveUrl = await bundle({entryPoint:path.join(root,manifest.entry),publicDir:path.join(root,'public'),
  outDir:path.join(root,'.cache/bundle'),webpackOverride: config => ({...config,
    resolve: {...config.resolve, modules:[...(modules?[modules]:[]),...(config.resolve?.modules||['node_modules'])]}})});
const browser = await openBrowser('chrome',{browserExecutable:browserPath});
try {
  const composition = await selectComposition({serveUrl,id:manifest.composition,inputProps,puppeteerInstance:browser});
  const scale = Number(value('--scale','1'));
  if (args.includes('--still')) {
    const frame = Number(value('--frame','0'));
    await renderStill({composition,serveUrl,inputProps,frame,scale,puppeteerInstance:browser,
      imageFormat:'png',output:path.resolve(output),logLevel:'error'});
  } else {
    const partial = args.includes('--from') || args.includes('--to');
    const range = partial ? [Number(value('--from','0')),Number(value('--to',String(composition.durationInFrames-1)))] : undefined;
    const visual = manifest.audio && !partial ? output.replace(/\.mp4$/,'.silent.mp4') : output;
    if (visual===output && manifest.audio && !partial) throw new Error('Muxed video output must end in .mp4');
    await renderMedia({composition,serveUrl,inputProps,puppeteerInstance:browser,codec:'h264',
      outputLocation:visual,frameRange:range,scale,concurrency:2,pixelFormat:'yuv420p',
      crf:18,muted:Boolean(manifest.audio),logLevel:'error'});
    if (manifest.audio && !partial) {
      const child = spawn('ffmpeg',['-v','warning','-y','-i',visual,'-i',path.join(root,manifest.audio),
        '-map','0:v:0','-map','1:a:0','-c','copy','-t',String(composition.durationInFrames/composition.fps),
        '-movflags','+faststart',output],{stdio:'inherit'});
      const [code] = await once(child,'close');
      if (code!==0) throw new Error(`ffmpeg mux exited ${code}`);
    }
  }
  console.log(JSON.stringify({status:'PASS',output,composition:composition.id,
    dimensions:[composition.width*scale,composition.height*scale],fps:composition.fps,
    note:manifest.audio?'Generic runner omits the archival multi-exposure shutter pass; see legacy reproduction reference.':undefined}));
} finally {await browser.close({silent:true});}
