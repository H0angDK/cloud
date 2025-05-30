// Initialize the map
const map = L.map('map').setView([55.7558, 37.6173], 13); // Moscow coordinates as example

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Simulated transport positions
const transportPositions = [
    { id: 1, lat: 55.7558, lng: 37.6173, type: 'bus' },
    { id: 2, lat: 55.7517, lng: 37.6178, type: 'tram' },
    { id: 3, lat: 55.7520, lng: 37.6150, type: 'bus' }
];

// Create markers for each transport
const markers = {};
transportPositions.forEach(transport => {
    const marker = L.marker([transport.lat, transport.lng])
        .bindPopup(`Transport #${transport.id} (${transport.type})`);
    markers[transport.id] = marker;
    marker.addTo(map);
});

// Simulate movement
function updatePositions() {
    transportPositions.forEach(transport => {
        // Add small random movement
        transport.lat += (Math.random() - 0.5) * 0.001;
        transport.lng += (Math.random() - 0.5) * 0.001;
        
        // Update marker position
        markers[transport.id].setLatLng([transport.lat, transport.lng]);
    });
}

// Update positions every 2 seconds
setInterval(updatePositions, 2000); 