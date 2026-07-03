import cv2
import serial
import asyncio

ser = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)

def uart_send(data):
    try:
        if not ser.is_open:
            ser.open()
        send_data = f"{data}\n"
        ser.write(send_data.encode("utf-8"))
        print(data)
    except Exception as e:
        print(e)

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
        else:
            self.prev = None
            self.cont = 0

async def main():

    # カメラの開始 (0番は通常インカメ)
    cap = cv2.VideoCapture(0)
    processor = ArUcoProcess(threshold=3)

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("終了")
                break

            result = processor.frame_process(frame)
            if result is not None:
                print("読み取り成功：", result)

                try:
                    uart_send(result)
                    print("送信成功", result)
                except Exception as e:
                    print("error", e)

            # 画面表示
            # cv2.imshow('Kiha 110 Safety System', frame)

            # 'q'キーで終了
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            await asyncio.sleep(0.01)
    finally:
        cap.release()
        cv2.destroyAllWindows()
        if ser.is_open:
            ser.close()

asyncio.run(main())
