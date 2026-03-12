from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
from fastapi.responses import HTMLResponse
from typing import List

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket:WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://172.27.168.234:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };

            //const message = document.getElementById("messages")

            ws.onopen = (event) =>{
                console.log("connected")
            }

            // ws.onmessage = (event) => {
            //     const msg = event.data;
            //
            //     var messages = document.getElementById('messages')
            //     var message = document.createElement('li')
            //     var content = document.createTextNode(event.data)
            //     message.appendChild(content)
            // }

            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                console.log(input.value)
                //message = input.value
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.get("/message")
def root():
    return {"message": "hello,world!"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    print("Connected!")
    try:
        await manager.broadcast(f"Connected!")
        while True:
            # 接続を維持するために待機
            data = await websocket.receive_text()
            # フロントエンドに送信
            await manager.broadcast(f"message text was {data}")
            print(f"message: {data}")
    except Exception as e:
        print(f"接続終了: {e}")

if __name__ == "__main__":
    # 0.0.0.0で待ち受けることで外部(Pico)から接続可能にする
    uvicorn.run(app, host="0.0.0.0", port=8000)
