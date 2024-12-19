from confluent_kafka import Consumer

consumer = Consumer(
    {
        "bootstrap.servers": "localhost:9092",
        "group.id": "test-group",
        "auto.offset.reset": "earliest",
    }
)

print("Подписка на топик...")
consumer.subscribe(["test-topic"])

print("Ожидание сообщения...")
for _ in range(10):  # Пробуем 10 раз с интервалом 1 секунда
    msg = consumer.poll(1.0)  # Ждем 1 секунду
    if msg is None:
        print("Нет новых сообщений...")
        continue
    if msg.error():
        print(f"Ошибка: {msg.error()}")
    else:
        print(
            f"Топик: {msg.topic()}, Раздел: {msg.partition()}, Смещение: {msg.offset()}"
        )
        print(f"Получено сообщение: {msg.value().decode('utf-8')} (ключ: {msg.key()})")
        break

consumer.close()
