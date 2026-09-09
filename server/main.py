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
        "now_edge": None,
        "direction": None,
        "mc": 0,
    },
    1: {
        "id": 1,
        "speed": 0,
        "limit": 0,
        "position": -1,
        "now_edge": None,
        "direction": None,
        "mc": 0,
    },
    2: {
        "id": 2,
        "speed": 0,
        "limit": 0,
        "position": -1,
        "now_edge": None,
        "direction": None,
        "mc": 0,
    }
}   
topics = [("train/0", 0), ("train/1", 0), ("train/2", 0), ("train/+/limit", 0), ("emergency", 1), ("map/now", 0)]

map_now = {}
nodes = {}
edges = {}
node_edges = defaultdict(list)

with open("data/maps.json", "r", encoding="utf-8") as f:
    MAPS_DATA = json.load(f)

#現在のマップの状態を管理
def build_graph(map_now):
    global nodes, edges, node_edges

    if not map_now:
        return

    nodes = {n["id"]: n for n in map_now["nodes"]}
    edges = {r["id"]: {**r, "now_train": None} for r in map_now["routes"]}
    # print("node",nodes)
    # print("edge",edges)
    node_edges = defaultdict(list)
    for e in edges.values():
        node_edges[e["from"]].append(e["id"])
        node_edges[e["to"]].append(e["id"])
    # print(node_edges)

#edgeの値を更新
def update_now_edge(old_edge, new_edge):
    for edge in edges.values():
        if edge["from"] == old_edge and edge["to"] == new_edge:
            return edge["id"]
        if edge["from"] == new_edge and edge["to"] == old_edge:
            return edge["id"]
    return None

#在線処理
def update_train_position(train_id, new_edge):
    global edges, trains
    #リセット
    for edge in edges.values():
        if edge["now_train"] == train_id:
            edge["now_train"] = None
            break
    #新しい位置で配置
    if new_edge is not None:
        edges[new_edge]["now_train"] = train_id
    
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

def on_message(client, data, msg):
    global trains, map_now
    print("onMessage!")
    print("edge", edges)
    print("node",nodes)
    print("no_ed", node_edges)
    try:
        payload = json.loads(msg.payload)
        if msg.topic.startswith("train/"):
            train_id = int(msg.topic.split("/")[1])

            if msg.topic.endswith("/limit"):
                trains[train_id]["limit"] = payload.get("limit", 0)
            else:
                trains[train_id]["speed"] = payload.get("speed", 0)
                trains[train_id]["direction"] = payload.get("direction", None)
                trains[train_id]["mc"] = payload.get("mc", 0)

                now_node = trains[train_id]["position"]
                new_node = payload.get("position", None)
                if new_node is not None and new_node != now_node:
                    new_edge = update_now_edge(now_node, new_node)
                    if new_edge is not None:
                        trains[train_id]["now_edge"] = new_edge
                        #マップ側での在線位置を更新
                        update_train_position(train_id, new_edge)
                    else:
                        print(f"train {train_id}: no edge between {now_node} -> {new_node}")
                    trains[train_id]["position"] = new_node


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
            build_graph(map_now)
            # print("map_now:",  payload)

    except Exception as e:
        print("json parse error", e)

client = mqtt.Client() 
client.on_connect = on_connect 

client.on_message = on_message 
client.connect(BROKER, port, 60)
client.loop_forever()
