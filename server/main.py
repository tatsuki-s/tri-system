#加工サーバー用ファイル
import json
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os

#車両間に応じた速度制限
DISTANCE_LIMIT = {
    #±1 停止
    1: 0,
    #±2 警戒
    2: 80,
    #±3 注意
    3: 160,
    #±4 減速
    4: 240,
    #±5以上 進行
    5: 300
}

load_dotenv()

BROKER = os.getenv("BROKER")
print(BROKER)
port = 1883
trains = {
    0: {
        "id": 0,
        "speed": 0,
        "limit": 0,
        "position": -1,
        "direction": True,
        "mc": 0,
        "hazards": []
    },
    1: {
        "id": 1,
        "speed": 0,
        "limit": 0,
        "position": -1,
        "direction": True,
        "mc": 0,
        "hazards": []
    },
    2: {
        "id": 2,
        "speed": 0,
        "limit": 0,
        "position": -1,
        "direction": True,
        "mc": 0,
        "hazards": []
    }
}   
topics = [("train/0", 0), ("train/1", 0), ("train/2", 0), ("train/+/limit", 0), ("emergency", 1), ("map/now", 0)]

with open("data/maps.json", "r", encoding="utf-8") as f:
    MAPS_DATA = json.load(f)

def add_hazards(hazards):
    for i, data in trains.items():
        data["hazards"].append(hazards)
    print(trains)

def on_connect(client, data, flags, rc):
    print("connected")
    client.subscribe(topics)

    #最初のメッセージ
    client.publish("map", json.dumps(MAPS_DATA), qos=1, retain=True)

def update_limit(limit):
    for train_id in trains:
        trains[train_id]["limit"] = limit

    for i in range(len(trains)):
        client.publish(f"train/{i}/limit", limit)

def set_limits():
    #車両間隔が近いときの制限の適用
    for i, data in trains.items():
        for j, item in trains.items():
            if i != j:
                data["hazards"].append(item["position"])
            print(item)
    print("update hazards", trains)
        

def on_message(client, data, msg):
    global trains
    print("onMessage!")
    try:
        payload = json.loads(msg.payload)
        if msg.topic.startswith("train/"):
            train_id = int(msg.topic.split("/")[1])

            if msg.topic.endswith("/limit"):
                trains[train_id]["limit"] = payload.get("limit", 0)
            else:
                trains[train_id]["speed"] = payload.get("speed", 0)
                trains[train_id]["position"] = payload.get("position", None)
                trains[train_id]["direction"] = payload.get("direction", 0)
                trains[train_id]["mc"] = payload.get("mc", False)

            set_limits()

            client.publish("trains", json.dumps([trains[i] for i in range(3)])) 
        if msg.topic == "emergency":
            print(payload)
            is_emergency = payload.get("status", True)
            if is_emergency:
                update_limit(0)
            else:
                update_limit(300)
        if msg.topic == ("map/now"):
            default_hazards = payload["description"]["default_hazards"] 
            add_hazards(default_hazards)

    except Exception as e:
        print("json parse error", e)

client = mqtt.Client() 
client.on_connect = on_connect 

client.on_message = on_message 
client.connect(BROKER, port, 60)
client.loop_forever()
