import cv2
import asyncio
import websockets
import json

async def main():

    name = "hanbun"
    video_path = f"videos/{name}.mp4"
    url = "ws://localhost:8000/ws"

    prev = None
    count = 0
    sent = None

    # ArUcoの設定 (4x4の格子、50種類までのIDを使用する設定)
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

    # カメラの開始 (0番は通常インカメ)
    cap = cv2.VideoCapture(video_path)

    async with websockets.connect(url) as ws:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("終了")
                break

            # マーカーの検出
            corners, ids, rejectedImgPoints = detector.detectMarkers(frame)

            areas = {}
            Id = None
            ans = None

            # マーカーが見つかったら枠を描画
            if ids is not None:
                cv2.aruco.drawDetectedMarkers(frame, corners, ids)
                 
                for i in range(len(ids)):
                    c = corners[i][0]
                    area = cv2.contourArea(c)
                    Id = ids[i][0]
                    areas[str(Id)] = area
                    # print("ID:", ID, "面積:", area )

                # 大きく映ったほうだけ採用
                if len(ids) >= 2:
                    ans = int(max(areas, key=areas.get))
                    # print("大きいのは",ans, "面積は", max(areas.values()))
                    pass
                else:
                    ans = int(Id)

                # 3連続判定で鯖に送信
                if prev == ans:
                    if count >= 3 and sent != ans:
                        print("読み取り成功：", json.dumps({"data": ans}))
                        await ws.send(str(ans))
                        sent = ans
                    count += 1
                else:
                    count = 0
                prev = ans
                # print(sent)

            # else:
            #     count += 1
            # print(count)

            # 画面表示
            cv2.imshow('Kiha 110 Safety System Test', frame)

            # 'q'キーで終了
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            await asyncio.sleep(0.01)

    cap.release()
    cv2.destroyAllWindows()

asyncio.run(main())
