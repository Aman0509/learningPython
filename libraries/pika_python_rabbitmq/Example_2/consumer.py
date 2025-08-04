from mq_connector import MQConnector


def handle_message(ch, method, properties, body):
    print(f"[x] Received: {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


mq = MQConnector(broker_url="amqp://guest:guest@localhost:5672/")

# Register the queue for consuming
mq.consume_queue(queue="notify_queue", callback=handle_message, queue_max_priority=10)

# Start the consuming loop
mq.start_consuming()
