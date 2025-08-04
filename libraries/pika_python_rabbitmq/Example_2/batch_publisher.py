from mq_connector import MQConnector
import time

mq = MQConnector(broker_url="amqp://guest:guest@localhost:5672/")

queue_name = "batch_queue"

# Publish 100 sample messages
for i in range(100):
    message = f"Message {i + 1}"
    mq.push_message(queue=queue_name, message=message)
    print(f"Published: {message}")
    time.sleep(0.1)  # simulate some delay
