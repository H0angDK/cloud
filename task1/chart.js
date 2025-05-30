// Get the canvas element
const ctx = document.getElementById('loadChart').getContext('2d');

// Sample data for route load
const routeData = {
    labels: ['Route 1', 'Route 2', 'Route 3', 'Route 4', 'Route 5'],
    datasets: [{
        label: 'Current Load',
        data: [65, 45, 80, 30, 55],
        backgroundColor: 'rgba(54, 162, 235, 0.5)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1
    }]
};

// Create the chart
const loadChart = new Chart(ctx, {
    type: 'bar',
    data: routeData,
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
                max: 100,
                title: {
                    display: true,
                    text: 'Load Percentage'
                }
            }
        },
        plugins: {
            title: {
                display: true,
                text: 'Route Load Distribution'
            }
        }
    }
});

// Simulate data updates
function updateChartData() {
    const newData = routeData.datasets[0].data.map(value => {
        // Add random variation to the load
        return Math.max(0, Math.min(100, value + (Math.random() - 0.5) * 10));
    });
    
    loadChart.data.datasets[0].data = newData;
    loadChart.update();
}

// Update chart every 3 seconds
setInterval(updateChartData, 3000); 