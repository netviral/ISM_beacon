const express = require('express');
const http = require('http');
const path = require('path');
const { spawn } = require('child_process');

const app = express();
const port = 3000;

// Serve static files (e.g., CSS)
app.use(express.static(path.join(__dirname, 'public')));

// Route to serve the HTML page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Stream the MJPG feed from the Raspberry Pi
app.get('/stream', (req, res) => {
  const mjpgStreamer = spawn('mjpg_streamer', [
    '-i', '/usr/local/lib/mjpg-streamer/input_uvc.so',
    '-o', '/usr/local/lib/mjpg-streamer/output_http.so', 
    '-p', '8080',
    '-w', '/usr/local/www'
  ]);

  mjpgStreamer.stdout.pipe(res);
  mjpgStreamer.stderr.on('data', (data) => {
    console.error(`Error: ${data}`);
  });

  mjpgStreamer.on('close', (code) => {
    console.log(`MJPG Streamer exited with code ${code}`);
    res.end();
  });

  req.on('close', () => mjpgStreamer.kill()); // Clean up when the request ends
});

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
