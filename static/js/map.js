document.addEventListener("DOMContentLoaded", function () {
  const map = L.map('map').setView([-2.9057, -41.7754], 13);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);
  L.marker([-2.9057, -41.7754]).addTo(map)
    .bindPopup('Condomínio em Parnaíba')
    .openPopup();
});
