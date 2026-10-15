// Nikoi shooter — clicker by Олиньо!!
console.log('Олиньо!! тип проекта: game');

const arena = document.getElementById('arena');
const scoreEl = document.getElementById('score');
const comboEl = document.getElementById('combo');
const timeEl = document.getElementById('time');
const accEl = document.getElementById('acc');
const bestEl = document.getElementById('best');
const playBtn = document.getElementById('play');
const resetBtn = document.getElementById('reset');
const msgEl = document.getElementById('message');

const SKINS = ['👾','🤖','👽','🎃','🛸','💀'];
const BONUS_SKIN = '🌟';

let score = 0, hits = 0, shots = 0, combo = 0, level = 1;
let timeLeft = 30, timer = null, spawner = null, playing = false;
let best = Number(localStorage.getItem('nikoi_best') || 0);
bestEl.textContent = best;

function updateHUD() {
  scoreEl.textContent = score;
  const mult = 1 + Math.floor(combo / 5);
  comboEl.textContent = 'x' + mult + ` (${combo})`;
  timeEl.textContent = timeLeft;
  accEl.textContent = shots === 0 ? '100%' : Math.round(hits / shots * 100) + '%';
}

function pew() {
  try {
    const ctx = pew.ctx || (pew.ctx = new (window.AudioContext || window.webkitAudioContext)());
    const o = ctx.createOscillator(), g = ctx.createGain();
    o.connect(g); g.connect(ctx.destination);
    o.type = 'square'; o.frequency.value = 600 + Math.random() * 600;
    g.gain.value = 0.08;
    o.start(); o.stop(ctx.currentTime + 0.08);
  } catch(e){}
}

function spawnTarget() {
  if (!playing) return;
  if (msgEl) msgEl.style.display = 'none';
  const t = document.createElement('div');
  t.className = 'target';
  const isBonus = Math.random() < 0.12;
  t.textContent = isBonus ? BONUS_SKIN : SKINS[Math.floor(Math.random() * SKINS.length)];
  if (isBonus) t.classList.add('bonus');

  const size = 64 - Math.min(level * 3, 24);
  t.style.width = t.style.height = size + 'px';
  const pad = 10;
  const x = pad + Math.random() * (arena.clientWidth - size - pad * 2);
  const y = pad + Math.random() * (arena.clientHeight - size - pad * 2);
  t.style.left = x + 'px'; t.style.top = y + 'px';

  const life = Math.max(1100 - level * 90, 450);
  const killTimer = setTimeout(() => t.remove(), life);

  t.addEventListener('pointerdown', (e) => {
    e.stopPropagation();
    if (!playing) return;
    clearTimeout(killTimer);
    shots++; hits++; combo++;
    const mult = 1 + Math.floor(combo / 5);
    const pts = (isBonus ? 50 : 10) * mult;
    score += pts;
    pew();
    boom(x, y, isBonus ? `+${pts} BONUS!` : `+${pts}`);
    if (hits % 5 === 0) { level++; restartSpawner(); }
    t.remove();
    updateHUD();
  });

  arena.appendChild(t);
}

function boom(x, y, text) {
  const b = document.createElement('div');
  b.className = 'boom';
  b.textContent = '💥 ' + text;
  b.style.left = x + 'px'; b.style.top = y + 'px';
  arena.appendChild(b);
  setTimeout(() => b.remove(), 400);
}

function restartSpawner() {
  if (spawner) clearInterval(spawner);
  const interval = Math.max(700 - level * 60, 250);
  spawner = setInterval(spawnTarget, interval);
}

function start() {
  reset(false);
  playing = true;
  playBtn.textContent = '⏸ СТОП';
  if (msgEl) msgEl.style.display = 'none';
  restartSpawner();
  timer = setInterval(() => {
    timeLeft--;
    updateHUD();
    if (timeLeft <= 0) gameOver();
  }, 1000);
  updateHUD();
}

function gameOver() {
  playing = false;
  clearInterval(timer); clearInterval(spawner);
  arena.querySelectorAll('.target').forEach(t => t.remove());
  if (score > best) {
    best = score;
    localStorage.setItem('nikoi_best', best);
    bestEl.textContent = best;
  }
  if (msgEl) {
    msgEl.style.display = 'flex';
    msgEl.textContent = `🏁 Финиш! Счёт: ${score} | Попаданий: ${hits} | Точность: ${accEl.textContent} — Жми СТАРТ ещё!`;
  }
  playBtn.textContent = '▶ ЕЩЁ РАЗ!';
  updateHUD();
}

function reset(full = true) {
  playing = false;
  clearInterval(timer); clearInterval(spawner);
  arena.querySelectorAll('.target,.boom').forEach(t => t.remove());
  score = 0; hits = 0; shots = 0; combo = 0; level = 1; timeLeft = 30;
  if (full && msgEl) { msgEl.style.display = 'flex'; msgEl.textContent = 'Жми СТАРТ и стреляй! 💥'; }
  playBtn.textContent = '▶ СТАРТ!';
  updateHUD();
}

arena.addEventListener('pointerdown', () => {
  if (!playing) return;
  shots++; combo = 0; // промах сбрасывает комбо
  updateHUD();
});

playBtn.addEventListener('click', () => playing ? gameOver() : start());
resetBtn.addEventListener('click', () => reset(true));
document.getElementById('play')?.addEventListener('click', () => console.log('click'));
updateHUD();
