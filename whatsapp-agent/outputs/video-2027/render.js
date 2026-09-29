// Renders video.html frame-by-frame (deterministic seek) and pipes to ffmpeg.
// usage: node render.js <ffmpeg> <audio.wav> <out.mp4>
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const { spawn } = require('child_process');
const path = require('path');
(async()=>{
  const [ff,wav,out]=process.argv.slice(2); const FPS=30, DUR=32;
  const enc=spawn(ff,['-y','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-','-i',wav,
    '-c:v','libx264','-preset','slow','-crf','21','-profile:v','high','-level','4.1','-pix_fmt','yuv420p',
    '-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',out],{stdio:['pipe','ignore','inherit']});
  const b=await chromium.launch();
  const p=await b.newPage({viewport:{width:1080,height:1920}});
  p.on('pageerror',e=>console.error('ERR',e.message));
  await p.goto('file://'+path.resolve(__dirname,'video.html'),{waitUntil:'networkidle'});
  await p.evaluate(()=>window.READY);
  for(let i=0;i<FPS*DUR;i++){
    await p.evaluate(t=>seek(t),i/FPS);
    const buf=await p.screenshot({type:'jpeg',quality:94});
    if(!enc.stdin.write(buf)) await new Promise(r=>enc.stdin.once('drain',r));
    if(i%150===0) console.error('frame',i);
  }
  enc.stdin.end(); await b.close();
  await new Promise(r=>enc.on('close',r)); console.error('done');
})();
