import { WebSocketServer } from "ws";

const wss = new WebSocketServer({ port: 8000});

wss.on('connection', (ws) => {
  ws.on('error', console.error);

  ws.on('message', (data) => {
    console.log('received: %s', data);
    wss.clients.forEach((client) => {
      if(client.readyState === 1){
        client.send(data.toString());
      }
    });
    ws.send(data.toString());
  });

  ws.send('Connected');
});

