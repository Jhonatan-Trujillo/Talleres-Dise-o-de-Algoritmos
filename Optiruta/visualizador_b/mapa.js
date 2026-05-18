const map = L.map('map', {
  center: [4.4389, -75.2322],
  zoom: 13,
  zoomControl: true
});

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors',
  maxZoom: 19
}).addTo(map);

let mapaData = null;
let pasosData = null;
let capas = { clientes: null, destinos: null, voraz: null, bt: null };
let capasActivas = { clientes: true, destinos: true, voraz: true, bt: false };

let animPasos = [];
let animStep = 0;
let animPlaying = false;
let animInterval = null;
let animSpeed = 20;
let animLayers = [];
let mejorRutaLayer = null;

function makeIcon(color, letra) {
  return L.divIcon({
    className: '',
    html: `<div style="
      width:28px;height:28px;border-radius:50%;
      background:${color};border:2px solid rgba(255,255,255,0.3);
      display:flex;align-items:center;justify-content:center;
      font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:600;
      color:white;box-shadow:0 2px 8px rgba(0,0,0,0.4);
    ">${letra}</div>`,
    iconSize: [28, 28],
    iconAnchor: [14, 14]
  });
}

document.getElementById('file-mapa').addEventListener('change', e => {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = ev => {
    try {
      mapaData = JSON.parse(ev.target.result);
      document.getElementById('file-mapa-ok').textContent = '✓ ' + file.name;
      renderMapa();
    } catch(err) {
      alert('Error al leer mapa_data.json: ' + err.message);
    }
  };
  reader.readAsText(file);
});

document.getElementById('file-pasos').addEventListener('change', e => {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = ev => {
    try {
      pasosData = JSON.parse(ev.target.result);
      animPasos = pasosData.pasos;
      animStep = 0;
      document.getElementById('file-pasos-ok').textContent = '✓ ' + file.name + ' (' + animPasos.length.toLocaleString() + ' pasos)';
      document.getElementById('btn-play').disabled = false;
      document.getElementById('btn-reset-anim').disabled = false;
      document.getElementById('prog-tot').textContent = animPasos.length.toLocaleString();
      document.getElementById('anim-info').textContent = 'Listo — presiona Play';
    } catch(err) {
      alert('Error al leer pasos: ' + err.message);
    }
  };
  reader.readAsText(file);
});

function renderMapa() {
  if (!mapaData) return;
  Object.values(capas).forEach(c => { if (c) map.removeLayer(c); });

  const puntos = mapaData.puntos;
  const rutaVoraz = mapaData.ruta_voraz;

  document.getElementById('hdr-clientes').textContent = puntos.length;
  document.getElementById('hdr-voraz').textContent = (mapaData.distancia_voraz / 1000).toFixed(2);

  capas.clientes = L.layerGroup();
  puntos.forEach((p, i) => {
    const marker = L.marker([p.lat, p.lon], { icon: makeIcon('#6c63ff', i) });
    marker.bindPopup(`
      <b style="color:#6c63ff">${p.nombre}</b><br>
      <b>Producto:</b> ${p.producto}<br>
      <b>Peso:</b> ${p.peso_kg} kg<br>
      <b>Destino:</b> ${p.destino}
    `);
    capas.clientes.addLayer(marker);
  });
  capas.clientes.addTo(map);

  capas.destinos = L.layerGroup();
  const destinosVistos = new Set();
  puntos.forEach(p => {
    const key = `${p.destino_lat},${p.destino_lon}`;
    if (!destinosVistos.has(key)) {
      destinosVistos.add(key);
      const marker = L.marker([p.destino_lat, p.destino_lon], {
        icon: makeIcon('#00e5a0', '★')
      });
      marker.bindPopup(`<b style="color:#00e5a0">Destino</b><br>${p.destino}`);
      capas.destinos.addLayer(marker);
    }
  });
  capas.destinos.addTo(map);

  capas.voraz = L.layerGroup();
  const coordsVoraz = rutaVoraz.map(r => [r.lat, r.lon]);
  if (coordsVoraz.length > 1) {
    L.polyline(coordsVoraz, {
      color: '#6c63ff', weight: 3, opacity: 0.8
    }).addTo(capas.voraz);

    for (let i = 0; i < coordsVoraz.length - 1; i++) {
      const mid = [
        (coordsVoraz[i][0] + coordsVoraz[i+1][0]) / 2,
        (coordsVoraz[i][1] + coordsVoraz[i+1][1]) / 2
      ];
      L.circleMarker(mid, {
        radius: 3, color: '#6c63ff', fillColor: '#6c63ff', fillOpacity: 1, weight: 0
      }).addTo(capas.voraz);
    }
  }
  capas.voraz.addTo(map);

  if (coordsVoraz.length > 0) {
    map.fitBounds(L.latLngBounds(coordsVoraz), { padding: [40, 40] });
  }

  renderInfoPanel(puntos);
}

function renderInfoPanel(puntos) {
  const scroll = document.getElementById('info-scroll');
  scroll.innerHTML = '';
  puntos.forEach((p, i) => {
    const card = document.createElement('div');
    card.className = 'info-card';
    card.innerHTML = `
      <div class="info-card-title">[${i}] ${p.destino}</div>
      <div class="info-row"><span>Producto</span><span>${p.producto}</span></div>
      <div class="info-row"><span>Peso</span><span>${p.peso_kg} kg</span></div>
    `;
    card.style.cursor = 'pointer';
    card.onclick = () => map.setView([p.lat, p.lon], 16);
    scroll.appendChild(card);
  });
}

function toggleCapa(nombre) {
  if (!capas[nombre]) return;
  const btn = document.getElementById('btn-' + nombre);
  if (capasActivas[nombre]) {
    map.removeLayer(capas[nombre]);
    btn.classList.remove('active');
  } else {
    capas[nombre].addTo(map);
    btn.classList.add('active');
  }
  capasActivas[nombre] = !capasActivas[nombre];
}

function togglePlay() {
  animPlaying = !animPlaying;
  const btn = document.getElementById('btn-play');
  if (animPlaying) {
    btn.textContent = '⏸ Pause';
    btn.classList.add('active');
    startAnimLoop();
  } else {
    btn.textContent = '▶ Play';
    stopAnimLoop();
  }
}

function startAnimLoop() {
  stopAnimLoop();
  const delay = Math.max(1000 / animSpeed, 10);
  animInterval = setInterval(() => {
    if (animStep >= animPasos.length) { togglePlay(); return; }
    const batch = Math.ceil(animSpeed / 30);
    for (let b = 0; b < batch && animStep < animPasos.length; b++) {
      applyAnimStep(animPasos[animStep]);
      animStep++;
    }
    updateAnimUI();
  }, delay);
}

function stopAnimLoop() {
  if (animInterval) { clearInterval(animInterval); animInterval = null; }
}

function applyAnimStep(paso) {
  if (!mapaData) return;
  const puntos = mapaData.puntos;
  const tipo = paso.tipo;

  if (tipo === 'explorar') {
    const desde = paso.ruta[paso.ruta.length - 1];
    const hasta = paso.siguiente;
    if (desde < puntos.length && hasta < puntos.length) {
      const linea = L.polyline([
        [puntos[desde].lat, puntos[desde].lon],
        [puntos[hasta].lat, puntos[hasta].lon]
      ], { color: '#6c63ff', weight: 2, opacity: 0.6 });
      linea.addTo(map);
      animLayers.push(linea);
    }
    document.getElementById('anim-info').textContent = `→ explorar: ${desde} → ${hasta}`;

  } else if (tipo === 'backtrack') {
    const desde = paso.desde;
    const hasta = paso.ruta[paso.ruta.length - 1] ?? 0;
    if (desde < puntos.length && hasta < puntos.length) {
      const linea = L.polyline([
        [puntos[desde].lat, puntos[desde].lon],
        [puntos[hasta].lat, puntos[hasta].lon]
      ], { color: '#ffb347', weight: 1.5, opacity: 0.5, dashArray: '4,4' });
      linea.addTo(map);
      animLayers.push(linea);
    }
    document.getElementById('anim-info').textContent = `↩ backtrack desde ${desde}`;

  } else if (tipo === 'poda_distancia' || tipo === 'poda_peso') {
    const desde = paso.ruta[paso.ruta.length - 1];
    const hasta = paso.rechazado;
    if (desde < puntos.length && hasta < puntos.length) {
      const linea = L.polyline([
        [puntos[desde].lat, puntos[desde].lon],
        [puntos[hasta].lat, puntos[hasta].lon]
      ], { color: '#ff5c5c', weight: 1, opacity: 0.4, dashArray: '2,6' });
      linea.addTo(map);
      animLayers.push(linea);
      setTimeout(() => { try { map.removeLayer(linea); } catch(e){} }, 800);
    }
    document.getElementById('anim-info').textContent = `✂ poda ${tipo === 'poda_distancia' ? 'dist' : 'peso'}: ${hasta}`;

  } else if (tipo === 'mejor_ruta') {
    if (mejorRutaLayer) map.removeLayer(mejorRutaLayer);
    const coords = [...paso.ruta, 0]
      .filter(i => i < puntos.length)
      .map(i => [puntos[i].lat, puntos[i].lon]);
    mejorRutaLayer = L.polyline(coords, {
      color: '#00e5a0', weight: 4, opacity: 0.9
    }).addTo(map);
    animLayers.push(mejorRutaLayer);

    const dist = (paso.distancia / 1000).toFixed(2);
    document.getElementById('hdr-bt').textContent = dist;
    const vorazKm = mapaData ? (mapaData.distancia_voraz / 1000) : 0;
    document.getElementById('hdr-mejora').textContent = (vorazKm - dist).toFixed(2);
    document.getElementById('btn-bt').disabled = false;
    document.getElementById('anim-info').textContent = `★ mejor ruta: ${dist} km`;
  }
}

function updateAnimUI() {
  const pct = animPasos.length ? (animStep / animPasos.length * 100) : 0;
  document.getElementById('prog').style.width = pct + '%';
  document.getElementById('prog-cur').textContent = animStep.toLocaleString();
}

function resetAnim() {
  stopAnimLoop();
  animPlaying = false;
  animStep = 0;
  document.getElementById('btn-play').textContent = '▶ Play';
  document.getElementById('btn-play').classList.remove('active');
  document.getElementById('anim-info').textContent = 'Listo — presiona Play';
  updateAnimUI();
  animLayers.forEach(l => { try { map.removeLayer(l); } catch(e){} });
  animLayers = [];
  mejorRutaLayer = null;
}

function updateSpeed() {
  animSpeed = parseInt(document.getElementById('speed').value);
  document.getElementById('speed-val').textContent = animSpeed + '/s';
  if (animPlaying) startAnimLoop();
}