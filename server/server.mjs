import { WebSocketServer } from "ws";

const wss = new WebSocketServer({ port: 8000});
let jsonData

// 全データを管理
let activeData = {
  trains: {},
  points: {}
}

wss.on("connection", (ws) => {

  let nowTrainId = null

  ws.on("error", console.error);

  ws.on("message", (payload) => {
    jsonData = JSON.parse(payload);
    console.log("received", jsonData);
    // カメラのデータだったときの処理
    if (jsonData.type === "camera"){
      const trainId = jsonData.data.id;
      nowTrainId = trainId;
      activeData.trains[trainId] = jsonData.data;
      console.log("trains:", activeData.trains);
    };
  broadcast();
  });

  ws.on("close", () => {
    // idがリストに追加済みか確認
    if(nowTrainId !==null){
      console.log(activeData.trains[nowTrainId], "を削除")
      delete activeData.trains[nowTrainId];
    }
    
    broadcast();
  });

  ws.send("Connected");
});

const broadcast = () => {
  // 送信用データ
  const formatted = {
    trains: Object.values(activeData.trains),
  }
  const data = JSON.stringify(formatted);
  wss.clients.forEach(client => {
    if(client.readyState === 1){
      client.send(data);
      console.log("送信：", data)
    }
  });
};
