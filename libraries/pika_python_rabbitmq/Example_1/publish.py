# publish.py
import pika
import json
import uuid


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# declare the exchange
channel.exchange_declare(exchange="order", exchange_type="direct")

# sample order data
order = {
    "id": str(uuid.uuid4()),
    "user_email": "john.doe@example.com",
    "product": "Leather Jacket",
    "quantity": 1,
}

# publish the order to the exchange
channel.basic_publish(
    exchange="order",
    routing_key="order.notify",
    body=json.dumps({"user_email": order["user_email"]}),
)

print(" [x] Sent notify message")

channel.basic_publish(
    exchange="order", routing_key="order.report", body=json.dumps(order)
)

print(" [x] Sent report message")

connection.close()
