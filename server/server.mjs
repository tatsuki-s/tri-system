import { WebSocketServer } from "ws";

const wss = new WebSocketServer({ port: 8000});
let jsonData

let activeData = {
  trains: [],
  points: []
}

wss.on('connection', (ws) => {
  ws.on('error', console.error);

  ws.on('message', (data) => {
    console.log('received: %s', data);
    wss.clients.forEach((client) => {
      if(client.readyState === 1){
        jsonData = JSON.parse(data)
        console.log("json:",jsonData)
        if (jsonData.type === "camera"){
          activeData.trains.push(jsonData) 
          console.log(activeData)
        }

        client.send(data.toString());
      }
    });
    ws.send(data.toString());
  });

  ws.send('Connected');
});

