// ============================================================
// 홈지니 효과음
// - 청소/학습 청소 중: 위이이잉 모터 + 흡입음
// - 홈지니 터치: 짧은 귀여운 반응음
// - 청소 종료 효과음 없음
// - 충전 완료 효과음 없음
// ============================================================

let appAudioCtx = null;
let vacuumSound = null;

function getAppAudioContext(){
  if(!appAudioCtx){
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if(!AudioCtx) return null;

    appAudioCtx = new AudioCtx();
  }

  if(appAudioCtx.state === "suspended"){
    appAudioCtx.resume().catch(()=>{});
  }

  return appAudioCtx;
}


// 모바일 브라우저에서 첫 사용자 터치 이후 소리가 재생되도록 활성화
function unlockAppAudio(){
  const ctx = getAppAudioContext();
  if(!ctx) return;

  if(ctx.state === "suspended"){
    ctx.resume().catch(()=>{});
  }
}


// ============================================================
// 청소기 지속음
// ============================================================

function startVacuumSound(){
  if(vacuumSound) return;

  const ctx = getAppAudioContext();
  if(!ctx) return;


  // 전체 볼륨
  const master = ctx.createGain();

  master.gain.setValueAtTime(
    0.0001,
    ctx.currentTime
  );

  master.gain.exponentialRampToValueAtTime(
    0.045,
    ctx.currentTime + 0.22
  );

  master.connect(ctx.destination);


  // ----------------------------------------------------------
  // 1. 모터의 낮은 "웅——" 소리
  // ----------------------------------------------------------

  const motor = ctx.createOscillator();
  const motorGain = ctx.createGain();

  motor.type = "sawtooth";

  motor.frequency.setValueAtTime(
    108,
    ctx.currentTime
  );

  motorGain.gain.value = 0.34;

  motor
    .connect(motorGain)
    .connect(master);


  // ----------------------------------------------------------
  // 2. 흡입 팬의 "위이이잉" 고주파 성분
  // ----------------------------------------------------------

  const fan = ctx.createOscillator();
  const fanGain = ctx.createGain();

  fan.type = "sine";

  fan.frequency.setValueAtTime(
    410,
    ctx.currentTime
  );

  fanGain.gain.value = 0.16;

  fan
    .connect(fanGain)
    .connect(master);


  // ----------------------------------------------------------
  // 3. 너무 일정한 전자음처럼 들리지 않도록
  //    음높이를 아주 조금씩 흔들어줌
  // ----------------------------------------------------------

  const lfo = ctx.createOscillator();
  const lfoGain = ctx.createGain();

  lfo.type = "sine";
  lfo.frequency.value = 2.6;

  lfoGain.gain.value = 3.5;

  lfo.connect(lfoGain);

  lfoGain.connect(motor.frequency);
  lfoGain.connect(fan.frequency);


  // ----------------------------------------------------------
  // 4. 바닥을 실제로 흡입하는 듯한 약한 노이즈
  // ----------------------------------------------------------

  const bufferSize = Math.max(
    1,
    Math.floor(ctx.sampleRate * 1.4)
  );

  const noiseBuffer = ctx.createBuffer(
    1,
    bufferSize,
    ctx.sampleRate
  );

  const data = noiseBuffer.getChannelData(0);

  for(let i = 0; i < bufferSize; i++){
    data[i] = (Math.random() * 2 - 1) * 0.22;
  }


  const noise = ctx.createBufferSource();

  noise.buffer = noiseBuffer;
  noise.loop = true;


  const noiseFilter = ctx.createBiquadFilter();

  noiseFilter.type = "bandpass";
  noiseFilter.frequency.value = 720;
  noiseFilter.Q.value = 0.65;


  const noiseGain = ctx.createGain();

  noiseGain.gain.value = 0.08;


  noise
    .connect(noiseFilter)
    .connect(noiseGain)
    .connect(master);


  motor.start();
  fan.start();
  lfo.start();
  noise.start();


  vacuumSound = {
    master,
    motor,
    fan,
    lfo,
    noise,
    motorGain,
    fanGain,
    noiseGain
  };
}


// ============================================================
// 청소음 종료
// 별도 완료음 없이 위이이잉 소리만 자연스럽게 사라짐
// ============================================================

function stopVacuumSound(){
  if(!vacuumSound) return;

  const ctx = getAppAudioContext();

  const nodes = vacuumSound;

  vacuumSound = null;

  if(!ctx) return;


  const t = ctx.currentTime;


  try{
    nodes.master.gain.cancelScheduledValues(t);

    nodes.master.gain.setValueAtTime(
      Math.max(
        nodes.master.gain.value,
        0.0001
      ),
      t
    );

    nodes.master.gain.exponentialRampToValueAtTime(
      0.0001,
      t + 0.24
    );

  }catch(e){}


  setTimeout(()=>{

    ["motor","fan","lfo","noise"].forEach(key=>{

      try{
        nodes[key].stop();
      }catch(e){}

    });

    try{
      nodes.master.disconnect();
    }catch(e){}

  },280);
}


// ============================================================
// 홈지니 터치 반응음
// 귀여운 "삐뽀♪" 느낌
// ============================================================

function playHomeGenieTouchSound(){

  const ctx = getAppAudioContext();

  if(!ctx) return;


  const now = ctx.currentTime;


  const master = ctx.createGain();

  master.gain.setValueAtTime(
    0.0001,
    now
  );

  master.gain.exponentialRampToValueAtTime(
    0.075,
    now + 0.015
  );

  master.gain.exponentialRampToValueAtTime(
    0.0001,
    now + 0.34
  );

  master.connect(ctx.destination);


  function note(
    start,
    startFreq,
    endFreq,
    duration,
    volume
  ){

    const osc = ctx.createOscillator();
    const gain = ctx.createGain();


    osc.type = "sine";


    osc.frequency.setValueAtTime(
      startFreq,
      start
    );

    osc.frequency.exponentialRampToValueAtTime(
      endFreq,
      start + duration
    );


    gain.gain.setValueAtTime(
      0.0001,
      start
    );

    gain.gain.exponentialRampToValueAtTime(
      volume,
      start + 0.012
    );

    gain.gain.exponentialRampToValueAtTime(
      0.0001,
      start + duration
    );


    osc
      .connect(gain)
      .connect(master);


    osc.start(start);

    osc.stop(
      start + duration + 0.02
    );
  }


  // "삐-뽀♪"
  note(
    now,
    660,
    880,
    0.12,
    0.85
  );

  note(
    now + 0.105,
    900,
    1180,
    0.16,
    0.72
  );


  setTimeout(()=>{

    try{
      master.disconnect();
    }catch(e){}

  },420);
}


// 첫 사용자 터치에서 AudioContext 활성화
document.addEventListener(
  "pointerdown",
  unlockAppAudio,
  {
    once:true,
    capture:true
  }
);

document.addEventListener(
  "touchstart",
  unlockAppAudio,
  {
    once:true,
    capture:true,
    passive:true
  }
);
