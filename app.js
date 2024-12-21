const express = require('express');
const http = require('http');
const path = require('path');
const { spawn } = require('child_process');

const app = express();
const port = 3000;

// MJPG Streamer setup
let mjpgStreamer;
function startMJPGStreamer() {
  mjpgStreamer = spawn('mjpg_streamer', [
    '-i', '/usr/local/lib/mjpg-streamer/input_uvc.so -d /dev/video0 -r 640x480 -f 30 -n',
    '-o', '/usr/local/lib/mjpg-streamer/output_http.so -p 8080 -w /usr/local/www',
  ]);

  mjpgStreamer.stdout.on('data', (data) => console.log(`MJPG Streamer: ${data}`));
  mjpgStreamer.stderr.on('data', (data) => console.error(`MJPG Streamer Error: ${data}`));

  mjpgStreamer.on('close', (code) => {
    console.log(`MJPG Streamer exited with code ${code}`);
    mjpgStreamer = null;
  });
}


// Stop MJPG Streamer if running
function stopMJPGStreamer() {
  if (mjpgStreamer) {
    mjpgStreamer.kill();
    console.log('MJPG Streamer stopped.');
  }
}

// Serve static files (e.g., CSS)
app.use(express.static(path.join(__dirname, 'public')));

// Route to serve the HTML page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Route to check if the stream is running
app.get('/stream', (req, res) => {
  res.redirect('http://localhost:8080/?action=stream'); // Redirect to MJPG Streamer feed
});

// Start the server
const server = app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
  startMJPGStreamer(); // Start MJPG Streamer when the server starts
});

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('\nShutting down...');
  stopMJPGStreamer(); // Stop MJPG Streamer
  server.close(() => {
    console.log('Server closed.');
    process.exit(0);
  });
});
