// map.js
document.addEventListener("DOMContentLoaded", () => {
  const coords = [-2.9086316915186963, -41.76884957507456]; // Parnaíba, PI
  const map = L.map('map').setView(coords, 17);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);

  L.marker(coords)
    .addTo(map)
    .bindPopup('Condomínio em Parnaíba')
    .openPopup();

  L.circle(coords, {
    radius: 50,
    color: '#007bff',
    fillOpacity: 0.5
  }).addTo(map);
});