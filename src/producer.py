from kafka import KafkaProducer
import json

# Настройки продюсера
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_message(topic, message):
    producer.send(topic, value=message)
    producer.flush()
    print(f"Сообщение отправлено в топик '{topic}': {message}")

if __name__ == "__main__":
    topic = "chat-messages"
    message = {
        "sender": "user1",
        "receiver": "user2",
        "text": "Привет! Как дела?"
    }
    send_message(topic, message)
