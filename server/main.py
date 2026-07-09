#加工サーバー用ファイル
import json
import paho.mqtt.client as mqtt

BROKER = "localhost"
port = 1883
trains = {
    0: {
        "id": 0,
        "speed": 0,
        "limit": 0,
        "position": 0,
        "direction": True,
        "mc": 0
    },
    1: {
        "id": 1,
        "speed": 0,
        "limit": 0,
        "position": 0,
        "direction": True,
        "mc": 0
    },
    2: {
        "id": 2,
        "speed": 0,
        "limit": 0,
        "position": 0,
        "direction": True,
        "mc": 0
    }
}   
topics = [("train/0", 0), ("train/1", 0), ("train/2", 0), ("map", 0), ("train/+/limit", 0)]

def on_connect(client, data, flags, rc):
    print("connected")
    client.subscribe(topics)

def on_message(client, data, msg):
    global trains
    try:
        payload = json.loads(msg.payload)
        if msg.topic == "map":
            pass
        # if msg.topic == "trains":
            # for i in range(3):
            #     client.publish(f"train/{i}", json.dumps(payload[i]))
        if msg.topic.startswith("train/"):
            train_id = int(msg.topic.split("/")[1])

            if msg.topic.endswith("/limit"):
                trains[train_id]["limit"] = payload.get("limit", 0)
            else:
                trains[train_id]["speed"] = payload.get("speed", 0)
                trains[train_id]["position"] = payload.get("position", None)
                trains[train_id]["direction"] = payload.get("speed", 0)
                trains[train_id]["mc"] = payload.get("mc", False)

            client.publish("trains", json.dumps([trains[i] for i in range(3)])) 
    except Exception as e:
        print("json parse error", e)

client = mqtt.Client() 
client.on_connect = on_connect 

client.on_message = on_message 
client.connect(BROKER, port, 60)
client.loop_forever()
