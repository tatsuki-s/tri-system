import cv2

import asyncio
import websockets
import json

USE_WS = True
TRAIN_ID = 2

data = {
    "type": "camera",
    "data": {
        "id": TRAIN_ID,
        "status": "connected",
        "read_id": None
        }
    }

result_json = json.dumps({"data": data})

class ArUcoProcess:
    def __init__(self, threshold=3):
        self.prev = None
        self.count = 0
        self.sent = None
        self.threshold = 3

        # ArUcoの設定 (4x4の格子、50種類までのIDを使用する設定)
        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        parameters = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

    def frame_process(self, frame):
        # マーカーの検出
        # corners, ids, rejectedImgPoints = processor.detector.detectMarkers(frame)
        corners, ids, _ = self.detector.detectMarkers(frame)

        areas = {}
        read_id = None
        ans = None

        # マーカーが見つかったら枠を描画
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
             
            for i in range(len(ids)):
                c = corners[i][0]
                area = cv2.contourArea(c)
                read_id = ids[i][0]
                areas[str(read_id)] = area
                # print("ID:", ID, "面積:", area )

            # 大きく映ったほうだけ採用
            if len(ids) >= 2:
                ans = int(max(areas, key=areas.get))
                # print("大きいのは",ans, "面積は", max(areas.values()))
                pass
            else:
                ans = int(read_id)

            # 3連続判定で鯖に送信
            if self.prev == ans:
                if self.count >= self.threshold and self.sent != ans:
                    self.sent = ans
                    return ans
                self.count += 1
            else:
                self.count = 0
            self.prev = ans

async def main():

    name = "ginga-naname"
    video_path = f"videos/{name}.mp4"
    url = "ws://localhost:8000/ws"
    ws = None
    connect_wait = 300
    count = connect_wait
    # カメラの開始 (0番は通常インカメ)
    cap = cv2.VideoCapture(video_path)
    processor = ArUcoProcess(threshold=3)

    while True:
        if USE_WS and ws == None and count >= connect_wait:
            print("接続します")
            count = 0
            try:
                ws = await websockets.connect(url)
                data["data"]["status"] = "connected"
                await ws.send(json.dumps(data))
                print("接続成功")
            except Exception as e:
                print("接続失敗", e)
        ret, frame = cap.read()

        if not ret:
            print("終了")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            # 再度読み込み
            ret, frame = cap.read()
            if not ret:
                # 再度読み込んでも失敗する場合はループを抜ける（ファイル破損などの対策）
                print("動画の再読み込みに失敗しました。")
                break

        result = processor.frame_process(frame)
        if result is not None:
            print("読み取り成功：", result)

            if ws:
                try:
                    data["data"]["read_id"] = result
                    await ws.send(json.dumps(data))
                    print("送信成功", data)
                except Exception as e:
                    print("error", e)
                    ws = None

        # 画面表示
        cv2.imshow('Kiha 110 Safety System', frame)

        # 'q'キーで終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        count += 1
        await asyncio.sleep(0.01)

    cap.release()
    cv2.destroyAllWindows()

asyncio.run(main())
