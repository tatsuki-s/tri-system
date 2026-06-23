from mqtt import host, port, connect_mqtt
from datetime import datetime
import time

# MQTTブローカーの設定
topic = "test/{}"


def publish(client, topic, message):
    result = client.publish(topic, message)

    # ステータスコードを確認
    status = result[0]
    if status == 0:
        print(f"`{topic}`に`{message}`を送信しました")
    else:
        print(f"`{topic}`への送信に失敗しました")


def run():
    client = connect_mqtt(host, port)
    # パブリッシュ(10回)
    for i in range(10):
        publish(
            client,
            topic.format(i),
            datetime.now().strftime("%Y/%m/%d %H:%M:%S").encode("utf-8"),
        )
        time.sleep(1)  # 1秒停止


if __name__ == "__main__":
    run()
