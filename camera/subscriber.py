from mqtt import host, port, connect_mqtt

# サブスクライブするTopic
topic = 'test/+'  # ワイルドカードを使って複数のトピックをサブスクライブ


def run():
    client = connect_mqtt(host, port)
    client.subscribe(topic)
    client.loop_forever()


if __name__ == "__main__":
    run()
