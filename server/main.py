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
    i: {
        "id": i,
        "speed": 0,
        "limit": {"front": 0, "back": 0},
        "position": -1,
        "direction": None,
        "mc": 0,
    } for i in range(3)
}   
topics = [("train/0", 0), ("train/1", 0), ("train/2", 0), ("train/+/limit", 0), ("emergency", 1), ("map/now", 0)]

#現在の在線状況
main_line_map = {}
sub_main_line_map = {}

#副本線開通かどうか
sub_main_line = False

is_emergency = False

with open("data/maps.json", "r", encoding="utf-8") as f:
    MAPS_DATA = json.load(f)

#在線処理
def update_train_position(train_id, position, client):
    global main_line_map
    #前の在線情報を削除
    print(main_line_map["main"])
    for marker in main_line_map["main"].values():
        if marker["now_train"] == train_id:
            marker["now_train"] = None
            print(train_id, "updated")
        # print(marker)
    #最新の在線状況    
    main_line_map["main"][str(position)]["now_train"] = train_id
    client.publish("map/now", json.dumps(main_line_map))

    
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
    global trains, main_line_map, is_emergency
    print("onMessage!")
    try:
        payload = json.loads(msg.payload)
        if msg.topic.startswith("train/"):
            train_id = int(msg.topic.split("/")[1])

            if msg.topic.endswith("/limit"):
                trains[train_id]["limit"] = payload.get("limit", json.dumps({"front": 0, "back": 0}))
            else:
                trains[train_id]["speed"] = payload.get("speed", 0)
                trains[train_id]["direction"] = payload.get("direction", None)
                trains[train_id]["mc"] = payload.get("mc", 0)
                trains[train_id]["position"] = payload.get("position", -1) 

                if not payload.get("position") == -1:
                    update_train_position(train_id, trains[train_id]["position"], client)

            client.publish("trains", json.dumps([trains[i] for i in range(3)])) 
        if msg.topic == "emergency":
            print(payload)
            is_emergency = payload.get("status", True)
            if is_emergency:
                update_limit(0)
            else:
                update_limit(300)
        if msg.topic == ("map/now"):
            main_line_map = json.loads(json.dumps(payload))
            # print("main_line_map:",  payload)

    except Exception as e:
        print("json parse error", e)

client = mqtt.Client() 
client.on_connect = on_connect 

client.on_message = on_message 
client.connect(BROKER, port, 60)
client.loop_forever()
