import { WebSocketServer } from "ws";

const wss = new WebSocketServer({ port: 8000});
let jsonData

let activeData = {
  trains: {},
  points: {}
}

wss.on('connection', (ws) => {
  ws.on('error', console.error);

  ws.on('message', (payload) => {
    console.log("received");
    wss.clients.forEach((client) => {
      // 中身があるか
      if(client.readyState === 1){
        jsonData = JSON.parse(payload)
        console.log("json:",jsonData)
        // カメラのデータだったときの処理
        if (jsonData.type === "camera"){
          const trainId = jsonData.data.id
          activeData.trains[trainId] = jsonData.data
          console.log("trains:", activeData.trains)
        }

        client.send(JSON.stringify(activeData));
        console.log(JSON.stringify(activeData));
      }
    });
    // ws.send(payload.toString());
  });

  ws.send('Connected');
});

