const http = require('http');
const _ = require('lodash');

const port = process.env.PORT || 3001;

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
  res.end(_.upperFirst('github actions test ran successfully'));
});

server.listen(port, () => {
  console.log(`server listening on port ${port}`);
});
