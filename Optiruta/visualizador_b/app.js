const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');

let pasos = [];
let N = 0;
let currentStep = 0;
let playing = false;
let playInterval = null;
let stepsPerSec = 30;

let counters = { explore: 0, backtrack: 0, poda: 0, mejor: 0 };
let bestRoute = null;
let bestDist = Infinity;

let nodePositions = [];
let currentPath = [];
let prunedFlashes = [];

const COLORS = {
  explorar: '#6c63ff',
  backtrack: '#ffb347',
  poda_distancia: '#ff5c5c',
  poda_peso: '#ff6584',
  mejor_ruta: '#00e5a0',
  node_default: '#1a1a26',
  node_active: '#6c63ff',
  node_start: '#00e5a0',
  edge_active: '#6c63ff',
  text: '#e8e8f0',
  muted: '#6b6b80',
  border: 'rgba(255,255,255,0.1)'
};

function resizeCanvas() {
  const wrap = canvas.parentElement;
  canvas.width = wrap.clientWidth;
  canvas.height = wrap.clientHeight;
  draw();
}

window.addEventListener('resize', resizeCanvas);
resizeCanvas();

function computeNodePositions() {
  nodePositions = [];
  const W = canvas.width, H = canvas.height;
  const cx = W / 2, cy = H / 2;
  const r = Math.min(W, H) * 0.35;
  for (let i = 0; i < N; i++) {
    const angle = (2 * Math.PI * i / N) - Math.PI / 2;
    nodePositions.push({
      x: cx + r * Math.cos(angle),
      y: cy + r * Math.sin(angle),
      id: i
    });
  }
}

function draw() {
  const W = canvas.width, H = canvas.height;
  ctx.clearRect(0, 0, W, H);

  if (N === 0) {
    ctx.fillStyle = COLORS.muted;
    ctx.font = '14px JetBrains Mono';
    ctx.textAlign = 'center';
    ctx.fillText('Carga pasos_backtracking.json para comenzar', W/2, H/2);
    return;
  }

  const now = Date.now();

  // Conexiones fantasma
  ctx.strokeStyle = 'rgba(255,255,255,0.03)';
  ctx.lineWidth = 0.5;
  for (let i = 0; i < N; i++) {
    for (let j = i+1; j < N; j++) {
      ctx.beginPath();
      ctx.moveTo(nodePositions[i].x, nodePositions[i].y);
      ctx.lineTo(nodePositions[j].x, nodePositions[j].y);
      ctx.stroke();
    }
  }

  // Aristas activas
  for (let k = 0; k < currentPath.length - 1; k++) {
    const a = nodePositions[currentPath[k]];
    const b = nodePositions[currentPath[k+1]];
    if (!a || !b) continue;
    ctx.beginPath();
    ctx.moveTo(a.x, a.y);
    ctx.lineTo(b.x, b.y);
    ctx.strokeStyle = COLORS.edge_active;
    ctx.lineWidth = 2;
    ctx.globalAlpha = 0.7;
    ctx.stroke();
    ctx.globalAlpha = 1;

    // Flecha dirección
    const dx = b.x - a.x, dy = b.y - a.y;
    const len = Math.sqrt(dx*dx + dy*dy);
    const mx = (a.x+b.x)/2, my = (a.y+b.y)/2;
    const ux = dx/len, uy = dy/len;
    ctx.beginPath();
    ctx.moveTo(mx - ux*6 - uy*4, my - uy*6 + ux*4);
    ctx.lineTo(mx + ux*6, my + uy*6);
    ctx.lineTo(mx - ux*6 + uy*4, my - uy*6 - ux*4);
    ctx.strokeStyle = COLORS.edge_active;
    ctx.lineWidth = 1.5;
    ctx.stroke();
  }

  // Flashes de poda
  prunedFlashes = prunedFlashes.filter(f => now - f.t < 600);
  for (const f of prunedFlashes) {
    const a = nodePositions[f.from];
    const b = nodePositions[f.to];
    if (!a || !b) continue;
    const alpha = 1 - (now - f.t) / 600;
    ctx.beginPath();
    ctx.moveTo(a.x, a.y);
    ctx.lineTo(b.x, b.y);
    ctx.strokeStyle = f.color;
    ctx.lineWidth = 1.5;
    ctx.globalAlpha = alpha * 0.8;
    ctx.setLineDash([4, 4]);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.globalAlpha = 1;
  }

  // Nodos
  for (let i = 0; i < N; i++) {
    const pos = nodePositions[i];
    const isStart = i === 0;
    const isInPath = currentPath.includes(i);
    const isCurrent = currentPath.length > 0 && currentPath[currentPath.length-1] === i;
    const R = isCurrent ? 20 : isInPath ? 16 : isStart ? 18 : 13;

    if (isCurrent) {
      ctx.beginPath();
      ctx.arc(pos.x, pos.y, R + 8, 0, Math.PI*2);
      ctx.fillStyle = 'rgba(108,99,255,0.15)';
      ctx.fill();
    }

    ctx.beginPath();
    ctx.arc(pos.x, pos.y, R, 0, Math.PI*2);
    let fill = COLORS.node_default;
    if (isStart) fill = '#0a2a1a';
    else if (isCurrent) fill = '#1a1040';
    else if (isInPath) fill = '#151035';
    ctx.fillStyle = fill;
    ctx.fill();

    let stroke = COLORS.border;
    if (isStart) stroke = COLORS.node_start;
    else if (isCurrent) stroke = COLORS.node_active;
    else if (isInPath) stroke = 'rgba(108,99,255,0.5)';
    ctx.strokeStyle = stroke;
    ctx.lineWidth = isStart || isCurrent ? 2 : 1;
    ctx.stroke();

    ctx.fillStyle = isStart ? COLORS.node_start : isInPath ? COLORS.text : COLORS.muted;
    ctx.font = `${isCurrent ? '600' : '400'} ${isCurrent ? 12 : 10}px JetBrains Mono`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(i === 0 ? 'D' : i, pos.x, pos.y);

    const lx = pos.x + (pos.x > canvas.width/2 ? 28 : -28);
    const ly = pos.y + (pos.y > canvas.height/2 ? 20 : -20);
    ctx.fillStyle = isInPath ? 'rgba(108,99,255,0.8)' : 'rgba(107,107,128,0.5)';
    ctx.font = '9px JetBrains Mono';
    ctx.fillText(i === 0 ? 'depósito' : `c${i}`, lx, ly);
  }

  // Mejor ruta overlay
  if (bestRoute && bestRoute.length > 1) {
    for (let k = 0; k < bestRoute.length - 1; k++) {
      const a = nodePositions[bestRoute[k]];
      const b = nodePositions[bestRoute[k+1]];
      if (!a || !b) continue;
      ctx.beginPath();
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(b.x, b.y);
      ctx.strokeStyle = 'rgba(0,229,160,0.25)';
      ctx.lineWidth = 3;
      ctx.stroke();
    }
  }

  if (playing) requestAnimationFrame(draw);
}

function loadPasos(data) {
  pasos = data.pasos;
  N = data.n;
  currentStep = 0;
  counters = { explore: 0, backtrack: 0, poda: 0, mejor: 0 };
  bestRoute = null;
  bestDist = Infinity;
  currentPath = [0];
  prunedFlashes = [];

  computeNodePositions();
  updateUI();
  updateCounters();
  updateBest();

  document.getElementById('hdr-total').textContent = pasos.length.toLocaleString();
  document.getElementById('hdr-nodos').textContent = N;
  document.getElementById('prog-tot').textContent = pasos.length.toLocaleString();
  document.getElementById('btn-play').disabled = false;
  document.getElementById('btn-reset').disabled = false;
  document.getElementById('btn-step').disabled = false;

  draw();
}

function applyStep(paso) {
  const tipo = paso.tipo;
  if (tipo === 'explorar') {
    currentPath = [...paso.ruta, paso.siguiente];
    counters.explore++;
    addLog(`→ ${paso.ruta.join('→')} → ${paso.siguiente}`, 'explore', '→');
  } else if (tipo === 'backtrack') {
    currentPath = [...paso.ruta];
    counters.backtrack++;
    addLog(`↩ desde ${paso.desde} a ${paso.ruta[paso.ruta.length-1] ?? 0}`, 'backtrack', '↩');
  } else if (tipo === 'poda_distancia') {
    const from = paso.ruta[paso.ruta.length-1];
    prunedFlashes.push({ from, to: paso.rechazado, t: Date.now(), color: COLORS.poda_distancia });
    counters.poda++;
    addLog(`✂ poda dist: ${paso.rechazado}`, 'poda', '✂');
  } else if (tipo === 'poda_peso') {
    const from = paso.ruta[paso.ruta.length-1];
    prunedFlashes.push({ from, to: paso.rechazado, t: Date.now(), color: COLORS.poda_peso });
    counters.poda++;
    addLog(`✂ poda peso: ${paso.rechazado}`, 'poda', '✂');
  } else if (tipo === 'mejor_ruta') {
    bestRoute = [...paso.ruta, 0];
    bestDist = paso.distancia;
    counters.mejor++;
    addLog(`★ mejor: ${paso.distancia.toFixed(0)}m`, 'mejor', '★');
    updateBest();
  }
  updateCounters();
  updateUI();
}

function stepForward() {
  if (currentStep >= pasos.length) return;
  applyStep(pasos[currentStep]);
  currentStep++;
  if (!playing) draw();
}

function togglePlay() {
  playing = !playing;
  const btn = document.getElementById('btn-play');
  if (playing) {
    btn.textContent = '⏸ Pause';
    btn.classList.add('primary');
    startPlayLoop();
    requestAnimationFrame(draw);
  } else {
    btn.textContent = '▶ Play';
    stopPlayLoop();
    draw();
  }
}

function startPlayLoop() {
  stopPlayLoop();
  const delay = Math.max(1000 / stepsPerSec, 5);
  playInterval = setInterval(() => {
    if (currentStep >= pasos.length) { togglePlay(); return; }
    const batch = Math.ceil(stepsPerSec / 60);
    for (let b = 0; b < batch && currentStep < pasos.length; b++) {
      applyStep(pasos[currentStep]);
      currentStep++;
    }
    draw();
  }, delay);
}

function stopPlayLoop() {
  if (playInterval) { clearInterval(playInterval); playInterval = null; }
}

function resetAnim() {
  stopPlayLoop();
  playing = false;
  currentStep = 0;
  counters = { explore: 0, backtrack: 0, poda: 0, mejor: 0 };
  bestRoute = null;
  bestDist = Infinity;
  currentPath = [0];
  prunedFlashes = [];
  document.getElementById('btn-play').textContent = '▶ Play';
  document.getElementById('log').innerHTML = '';
  updateCounters();
  updateBest();
  updateUI();
  draw();
}

function updateSpeed() {
  stepsPerSec = parseInt(document.getElementById('speed').value);
  document.getElementById('speed-val').textContent = stepsPerSec + '/s';
  if (playing) startPlayLoop();
}

function updateUI() {
  document.getElementById('hdr-paso').textContent = currentStep.toLocaleString();
  const pct = pasos.length ? (currentStep / pasos.length * 100) : 0;
  document.getElementById('prog').style.width = pct + '%';
  document.getElementById('prog-cur').textContent = currentStep.toLocaleString();
}

function updateCounters() {
  document.getElementById('cnt-explore').textContent = counters.explore.toLocaleString();
  document.getElementById('cnt-back').textContent = counters.backtrack.toLocaleString();
  document.getElementById('cnt-poda').textContent = counters.poda.toLocaleString();
  document.getElementById('cnt-mejor').textContent = counters.mejor.toLocaleString();
}

function updateBest() {
  if (bestRoute) {
    document.getElementById('best-route').textContent = bestRoute.join(' → ');
    document.getElementById('best-dist').textContent = (bestDist/1000).toFixed(2) + ' km';
  } else {
    document.getElementById('best-route').textContent = '—';
    document.getElementById('best-dist').textContent = '';
  }
}

const MAX_LOG = 80;
function addLog(msg, type, icon) {
  const log = document.getElementById('log');
  const entry = document.createElement('div');
  entry.className = `log-entry log-${type}`;
  entry.innerHTML = `<span class="log-icon">${icon}</span><span>${msg}</span>`;
  log.appendChild(entry);
  while (log.children.length > MAX_LOG) log.removeChild(log.firstChild);
  log.scrollTop = log.scrollHeight;
}

document.getElementById('file-input').addEventListener('change', e => {
  const file = e.target.files[0];
  if (!file) return;
  document.getElementById('file-name').textContent = file.name;
  const reader = new FileReader();
  reader.onload = ev => {
    try {
      const data = JSON.parse(ev.target.result);
      loadPasos(data);
    } catch(err) {
      alert('Error al leer el JSON: ' + err.message);
    }
  };
  reader.readAsText(file);
});

draw();