#加工サーバー用ファイル
import json
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os
from collections import defaultdict

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
        "direction": None,
        "mc": 0,
    },
    1: {
        "id": 1,
        "speed": 0,
        "limit": 0,
        "position": -1,
        "direction": None,
        "mc": 0,
    },
    2: {
        "id": 2,
        "speed": 0,
        "limit": 0,
        "position": -1,
        "direction": None,
        "mc": 0,
    }
}   
topics = [("train/0", 0), ("train/1", 0), ("train/2", 0), ("train/+/limit", 0), ("emergency", 1), ("map/now", 0)]

map_now = {}
train_map = {}

with open("data/maps.json", "r", encoding="utf-8") as f:
    MAPS_DATA = json.load(f)

def on_connect(client, data, flags, rc):
    print("connected")
    client.subscribe(topics)

    #最初のメッセージ
    client.publish("map", json.dumps(MAPS_DATA), qos=1, retain=True)

def update_limit(new_limit, direction):
    global trains
    for train_id in trains:
        trains[train_id]["limit"]["direction"] = limit

    for i in range(len(trains)):
        client.publish(f"train/{i}/limit", json.dumps(trains[train_id]["limit"]))

def set_limits():
    #車両間隔が近いときの制限の適用
    pass
    # for i, data in trains.items():
    #     for j, item in train_map.items():
    #         if i != j:
    #             print(MAPS_DATA)
    #         print(item)
        

def on_message(client, data, msg):
    global trains, map_now
    print("onMessage!")
    try:
        payload = json.loads(msg.payload)
        if msg.topic.startswith("train/"):
            train_id = int(msg.topic.split("/")[1])

            if msg.topic.endswith("/limit"):
                trains[train_id]["limit"] = payload.get("limit", json.dumps({"front": 0, "back": 0}))
            else:
                trains[train_id]["speed"] = payload.get("speed", 0)
                trains[train_id]["position"] = payload.get("position", None)
                trains[train_id]["direction"] = payload.get("direction", None)
                trains[train_id]["mc"] = payload.get("mc", 0)

            client.publish("trains", json.dumps([trains[i] for i in range(3)])) 
        if msg.topic == "emergency":
            print(payload)
            is_emergency = payload.get("status", True)
            if is_emergency:
                update_limit(0)
            else:
                update_limit(300)
        if msg.topic == ("map/now"):
            map_now = json.loads(json.dumps(payload))
            # print("map_now:",  payload)

    except Exception as e:
        print("json parse error", e)

client = mqtt.Client() 
client.on_connect = on_connect 

client.on_message = on_message 
client.connect(BROKER, port, 60)
client.loop_forever()
