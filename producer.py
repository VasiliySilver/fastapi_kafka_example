from confluent_kafka import Producer

# Настройки продюсера
conf = {"bootstrap.servers": "localhost:9092"}

# Создание экземпляра продюсера
producer = Producer(conf)


# Функция обратного вызова для подтверждения доставки сообщения
def delivery_report(err, msg):
    if err is not None:
        print(f"Ошибка доставки сообщения: {err}")
    else:
        print(f"Сообщение доставлено: {msg.topic()} [{msg.partition()}]")


# Отправка сообщения
producer.produce(
    "test-topic", key="key1", value="Привет, Kafka!", callback=delivery_report
)

# Ожидание отправки всех сообщений
producer.flush()
