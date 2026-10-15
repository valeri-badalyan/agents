// Olinho Shooter - Space Defense
const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
const scoreEl = document.getElementById('score');
const livesEl = document.getElementById('lives');
const levelEl = document.getElementById('level');
const overlay = document.querySelector('.panel');
const ovTitle = document.getElementById('ovTitle');
const ovText = document.getElementById('ovText');

let running = false, paused = false;
let score = 0, lives = 3, level = 1;
let bullets = [], enemies = [], parts = [], stars = [];
let keys = {};
let player = { x: 480, y: 520, w: 44, h: 34, speed: 6, cd: 0 };
let spawnTimer = 0, lastTime = 0;

for (let i = 0; i < 120; i++) stars.push({ x: Math.random()*960, y: Math.random()*600, s: Math.random()*2+0.5, v: Math.random()*1.5+0.3 });

function beep(f=440,d=0.07,type='square',vol=0.06){
  try{
    const AC = window.AudioContext||window.webkitAudioContext;
    if(!AC) return;
    const ac = beep.ac || (beep.ac = new AC());
    const o = ac.createOscillator(), g = ac.createGain();
    o.type=type; o.frequency.value=f; g.gain.value=vol;
    o.connect(g); g.connect(ac.destination); o.start();
    g.gain.exponentialRampToValueAtTime(0.0001, ac.currentTime+d);
    o.stop(ac.currentTime+d);
  }catch(e){}
}

function reset(){
  score=0; lives=3; level=1; bullets=[]; enemies=[]; parts=[];
  player.x=480; player.y=520; spawnTimer=0;
  updateHUD();
}
function updateHUD(){
  scoreEl.textContent = score;
  livesEl.textContent = '❤️'.repeat(Math.max(0,lives)) || '💀';
  levelEl.textContent = level;
}
function spawn(){
  const r = Math.random();
  let e;
  if(r < 0.55) e = { x: Math.random()*900+30, y: -30, w: 38, h: 30, vy: 1.6+level*0.25, hp: 1, color: '#ff5252', pts: 50 };
  else if(r < 0.85) e = { x: Math.random()*900+30, y: -30, w: 30, h: 24, vy: 3+level*0.35, hp: 1, color: '#ffee58', pts: 80 };
  else e = { x: Math.random()*880+40, y: -40, w: 52, h: 40, vy: 1+level*0.2, hp: 3, color: '#ce93d8', pts: 150 };
  e.wob = Math.random()*Math.PI*2;
  enemies.push(e);
}
function shoot(){
  if(player.cd > 0) return;
  player.cd = 9;
  bullets.push({ x: player.x-3, y: player.y-18, w: 6, h: 16, vy: -11 });
  bullets.push({ x: player.x-3, y: player.y-18, w: 6, h: 16, vy: -11, dx: 0 });
  beep(880, 0.06, 'square', 0.05);
}
function explode(x,y,color,n=14){
  for(let i=0;i<n;i++) parts.push({ x, y, vx:(Math.random()-0.5)*6, vy:(Math.random()-0.5)*6, life:30+Math.random()*20, color });
}
function loop(t){
  if(!running) return;
  requestAnimationFrame(loop);
  if(paused) return;
  const dt = Math.min(33, t-lastTime || 16); lastTime=t;
  const step = dt/16.6;

  // stars
  ctx.fillStyle='#05071a'; ctx.fillRect(0,0,960,600);
  ctx.fillStyle='#fff';
  stars.forEach(s=>{ s.y+=s.v*step; if(s.y>600){s.y=0;s.x=Math.random()*960;} ctx.globalAlpha=0.7; ctx.fillRect(s.x,s.y,s.s,s.s); });
  ctx.globalAlpha=1;

  // player move
  if(keys['arrowleft']||keys['a']) player.x-=player.speed*step;
  if(keys['arrowright']||keys['d']) player.x+=player.speed*step;
  if(keys['arrowup']||keys['w']) player.y-=player.speed*0.8*step;
  if(keys['arrowdown']||keys['s']) player.y+=player.speed*0.8*step;
  player.x=Math.max(24,Math.min(936,player.x));
  player.y=Math.max(300,Math.min(570,player.y));
  if(keys[' ']) shoot();
  if(player.cd>0) player.cd-=step;

  // spawn
  spawnTimer-=step;
  if(spawnTimer<=0){ spawn(); spawnTimer=Math.max(12, 55-level*6); }
  level = 1+Math.floor(score/500);

  // bullets
  ctx.fillStyle='#00e5ff';
  bullets.forEach(b=>{ b.y+=b.vy*step; ctx.fillRect(b.x,b.y,b.w,b.h); });
  bullets=bullets.filter(b=>b.y>-30);

  // enemies
  enemies.forEach(e=>{
    e.wob+=0.05*step; e.y+=e.vy*step; e.x+=Math.sin(e.wob)*1.2*step;
    ctx.fillStyle=e.color;
    ctx.beginPath();
    ctx.moveTo(e.x, e.y+e.h);
    ctx.lineTo(e.x+e.w/2, e.y);
    ctx.lineTo(e.x+e.w, e.y+e.h);
    ctx.closePath(); ctx.fill();
    ctx.fillStyle='#00000088'; ctx.fillRect(e.x+6,e.y+e.h-10,e.w-12,4);
  });

  // collisions bullet-enemy
  for(let i=enemies.length-1;i>=0;i--){
    const e=enemies[i];
    for(let j=bullets.length-1;j>=0;j--){
      const b=bullets[j];
      if(b.x<e.x+e.w && b.x+b.w>e.x && b.y<e.y+e.h && b.y+b.h>e.y){
        bullets.splice(j,1); e.hp--;
        explode(b.x,b.y,'#00e5ff',6);
        if(e.hp<=0){ enemies.splice(i,1); score+=e.pts; explode(e.x+e.w/2,e.y+e.h/2,e.color,18); beep(220,0.12,'sawtooth',0.07); }
        else beep(330,0.05,'square',0.05);
        break;
      }
    }
  }

  // enemies hit player / bottom
  for(let i=enemies.length-1;i>=0;i--){
    const e=enemies[i];
    const hitPlayer = Math.abs(e.x+e.w/2-player.x)<36 && Math.abs(e.y+e.h/2-player.y)<30;
    if(hitPlayer || e.y>600){
      enemies.splice(i,1);
      if(hitPlayer || e.y>590){
        lives--; explode(player.x,player.y,'#ffb300',22); beep(120,0.3,'sawtooth',0.09);
        updateHUD();
        if(lives<=0){ gameOver(); return; }
      }
    }
  }

  // particles
  parts.forEach(p=>{ p.x+=p.vx*step; p.y+=p.vy*step; p.life-=step; ctx.globalAlpha=Math.max(0,p.life/40); ctx.fillStyle=p.color; ctx.fillRect(p.x,p.y,4,4); });
  ctx.globalAlpha=1;
  parts=parts.filter(p=>p.life>0);

  // player ship
  ctx.fillStyle='#00e5ff';
  ctx.beginPath();
  ctx.moveTo(player.x, player.y-22);
  ctx.lineTo(player.x-20, player.y+14);
  ctx.lineTo(player.x, player.y+4);
  ctx.lineTo(player.x+20, player.y+14);
  ctx.closePath(); ctx.fill();
  ctx.fillStyle='#ffb300';
  ctx.fillRect(player.x-3, player.y+4, 6, 12+Math.random()*8);

  updateHUD();
}

function start(){
  reset(); running=true; paused=false; lastTime=0;
  overlay.classList.add('hidden');
  beep(660,0.1); setTimeout(()=>beep(880,0.12),110);
  requestAnimationFrame(loop);
}
function gameOver(){
  running=false;
  ovTitle.textContent='💥 Игра окончена! Счёт: '+score;
  ovText.textContent='Уровень '+level+'. Жми Поехали, чтобы отомстить пришельцам! 🚀';
  overlay.classList.remove('hidden');
}

document.getElementById('startBtn').onclick=start;
document.getElementById('playBtn').onclick=start;
document.getElementById('restartBtn').onclick=start;
window.addEventListener('keydown',e=>{
  const k=e.key.toLowerCase();
  keys[k]=true;
  if(k===' ') e.preventDefault();
  if(k==='p'&&running) paused=!paused;
});
window.addEventListener('keyup',e=>{ keys[e.key.toLowerCase()]=false; });
canvas.addEventListener('mousemove',e=>{
  const r=canvas.getBoundingClientRect();
  player.x=(e.clientX-r.left)*(960/r.width);
});
canvas.addEventListener('mousedown',()=>{ if(running&&!paused) shoot(); else if(!running) start(); });
canvas.addEventListener('touchmove',e=>{
  e.preventDefault();
  const r=canvas.getBoundingClientRect();
  const t=e.touches[0];
  player.x=(t.clientX-r.left)*(960/r.width);
  player.y=(t.clientY-r.top)*(600/r.height);
},{passive:false});
canvas.addEventListener('touchstart',e=>{ if(running) shoot(); },{passive:true});

updateHUD();
console.log('Olinho shooter ready');
