# Transport Monitoring Dashboard

A static web interface for monitoring transport positions and route loads, hosted on LocalStack S3.

## Features

- Interactive map showing real-time transport positions
- Bar chart displaying route load distribution
- Responsive design for all devices
- Simulated data updates

## Prerequisites

- Python 3.6+
- LocalStack running locally
- pip (Python package manager)

## Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure LocalStack is running on your machine (default port: 4566)

3. Run the setup script to create the S3 bucket and upload files:
   ```bash
   python setup_s3.py
   ```

4. Access the dashboard at:
   ```
   http://localhost:4566/transport-dashboard/index.html
   ```

## Files

- `index.html` - Main HTML file
- `styles.css` - CSS styles
- `map.js` - Map functionality using Leaflet.js
- `chart.js` - Chart functionality using Chart.js
- `setup_s3.py` - Script to set up S3 bucket and upload files

## Notes

- The map shows simulated transport positions around Moscow
- Route load data is randomly generated and updates every 3 seconds
- The interface is fully responsive and works on mobile devices 