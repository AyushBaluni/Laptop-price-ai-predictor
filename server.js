const http = require('http');
const fs   = require('fs');
const path = require('path');

const PORT = 8787;
const ROOT = __dirname;

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css':  'text/css',
  '.js':   'application/javascript',
  '.json': 'application/json',
  '.csv':  'text/csv',
  '.png':  'image/png',
};

http.createServer((req, res) => {
  const filePath = path.join(ROOT, req.url === '/' ? '/laptop_price_predictor.html' : req.url);
  const ext = path.extname(filePath);
  fs.readFile(filePath, (err, data) => {
    if (err) { res.writeHead(404); res.end('Not found'); return; }
    res.writeHead(200, { 'Content-Type': MIME[ext] || 'text/plain' });
    res.end(data);
  });
}).listen(PORT, '127.0.0.1', () => {
  console.log(`Server running at http://localhost:${PORT}/`);
});
