import threading
import time
from mq_connector import MQConnector

mq = MQConnector(broker_url="amqp://guest:guest@localhost:5672/", prefetch_count=20)
queue_name = "batch_queue"

message_buffer = []
buffer_lock = threading.Lock()
batch_size = 20
batch_timeout = 5
last_batch_time = time.time()


def safe_acknowledge_batch(messages):
    for body, method in messages:
        print(body.decode())
        mq.channel.basic_ack(delivery_tag=method.delivery_tag)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Use this code to verify `prefetch_count` behavior #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# def safe_acknowledge_batch(messages_to_ack):
#     print(f"\n✅ Processing batch of {len(messages_to_ack)} messages:")
#     for i, (body, method) in enumerate(messages_to_ack, 1):
#         print(f"Message {i}: {body}")

#     # Simulate processing delay
#     time.sleep(10)  # <- Add this

#     for _, method in messages_to_ack:
#         mq.channel.basic_ack(delivery_tag=method.delivery_tag)


def batch_processor():
    global last_batch_time
    while True:
        time.sleep(1)
        with buffer_lock:
            time_passed = time.time() - last_batch_time
            if message_buffer and (
                len(message_buffer) >= batch_size or time_passed >= batch_timeout
            ):
                print(f"\nProcessing batch of {len(message_buffer)} messages:")
                messages_to_ack = message_buffer.copy()
                message_buffer.clear()
                last_batch_time = time.time()

                # Schedule the safe acknowledgment inside the main thread
                mq.connection.add_callback_threadsafe(
                    lambda: safe_acknowledge_batch(messages_to_ack)
                )


def callback(ch, method, properties, body):
    global last_batch_time
    with buffer_lock:
        message_buffer.append((body, method))
        if len(message_buffer) >= batch_size:
            last_batch_time = time.time()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Use this code to verify `prefetch_count` behavior #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# def callback(ch, method, properties, body):
#     with buffer_lock:
#         print(f"[RECEIVED] {body.decode()}")
#         message_buffer.append((body.decode(), method))
#         if len(message_buffer) >= batch_size:
#             global last_batch_time
#             last_batch_time = time.time()

threading.Thread(target=batch_processor, daemon=True).start()
mq.consume_queue(queue=queue_name, callback=callback)
mq.start_consuming()
