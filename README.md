Шаг 1:  Запуск Kafka + Zookeeper
```bash
cd docker && docker compose up -d
```

Шаг 2: Создание топика для чата
Для чата потребуется топик, в который будем отправлять сообщения.

Запустите консоль Kafka CLI (если установлен Kafka CLI на хосте или внутри контейнера):

```bash
docker exec -it kafka kafka-topics --create --topic chat-messages --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
```

Шаг 3: Установка зависимостей
```bash 
python -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate     # Для Windows
poetry install
```

Шаг 4: Создадим файл src/producer.py
```bash
from kafka import KafkaConsumer
import json

# Настройки потребителя
consumer = KafkaConsumer(
    'chat-messages',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    group_id='chat-consumers'
)

def consume_messages():
    print("Ожидание сообщений...")
    for message in consumer:
        print(f"Получено сообщение: {message.value}")

if __name__ == "__main__":
    consume_messages()
```

Шаг 5: Запустим его
```bash
python src/producer.py
```
