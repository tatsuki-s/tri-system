import cv2

count = 0
video_path = "videos/aruco_sample.mp4"
prev = None

# ArUcoの設定 (4x4の格子、50種類までのIDを使用する設定)
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

# カメラの開始 (0番は通常インカメ)
cap = cv2.VideoCapture(video_path)

while True:
    ret, frame = cap.read()
    if not ret:
        print("終了")
        break

    # マーカーの検出
    corners, ids, rejectedImgPoints = detector.detectMarkers(frame)

    areas = {}
    read = None
    Id = None

    # マーカーが見つかったら枠を描画
    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
         
        ans = None
        for i in range(len(ids)):
            c = corners[i][0]
            area = cv2.contourArea(c)
            Id = ids[i][0]
            areas[str(Id)] = area
            # print("ID:", ID, "面積:", area )
        if len(ids) >= 2:
            ans = max(areas, key=areas.get)
            # print("大きいのは",ans, "面積は", max(areas.values()))
            pass
        else:
            ans = Id
            # print("読み取ったのは:", ans)
        prev = ans
        print(ans)
    # else:
    #     count += 1
    # print(count)


    # 画面表示
    cv2.imshow('Kiha 110 Safety System Test', frame)

    # 'q'キーで終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
