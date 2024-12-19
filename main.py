from fastapi import FastAPI
from confluent_kafka import Producer, Consumer
import asyncio

app = FastAPI()

producer = Producer({'bootstrap.servers': 'localhost:9092'})
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'chat-group',
    'auto.offset.reset': 'earliest'
})

@app.post("/send-message/")
async def send_message(user: str, message: str):
    def delivery_report(err, msg):
        if err:
            print(f"Ошибка доставки: {err}")
        else:
            print(f"Сообщение доставлено: {msg.topic()} [{msg.partition()}]")

    print(f"Отправка сообщения: пользователь={user}, сообщение={message}")
    producer.produce('chat-messages', key=user, value=message, callback=delivery_report)
    producer.flush()
    return {"status": "Message sent"}

@app.get("/get-messages/")
async def get_messages():
    consumer.subscribe(['chat-messages'])
    messages = []
    print("Чтение сообщений из топика...")
    for _ in range(10):  # Считать до 10 сообщений
        msg = consumer.poll(1.0)
        if msg is None:
            print("Нет новых сообщений...")
            continue
        if msg.error():
            print(f"Ошибка чтения сообщения: {msg.error()}")
            return {"error": str(msg.error())}
        else:
            decoded_message = msg.value().decode('utf-8')
            print(f"Получено сообщение: {decoded_message}")
            messages.append(decoded_message)
    return {"messages": messages}

