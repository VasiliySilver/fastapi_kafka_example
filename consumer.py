from confluent_kafka import Consumer, KafkaException

# Настройки консюмера
conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "test-group",
    "auto.offset.reset": "earliest",
}

# Создание экземпляра консюмера
consumer = Consumer(conf)

# Подписка на топик
consumer.subscribe(["test-topic"])

print("Ожидание сообщений...")
try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaException._PARTITION_EOF:
                print("Достигнут конец раздела")
            else:
                print(f"Ошибка: {msg.error()}")
        else:
            print(
                f'Получено сообщение: ключ={msg.key().decode("utf-8")}, значение={msg.value().decode("utf-8")}'
            )
except KeyboardInterrupt:
    pass
finally:
    # Закрытие консюмера
    consumer.close()
