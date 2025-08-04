"""
How RabbitMQ Priority Queues Work (Important Detail)

- Priority affects message delivery only when multiple messages are waiting in the queue.
- If you consume messages immediately after publishing each, the priority has no chance to reorder them — they just go straight through.
- RabbitMQ doesn't delay lower-priority messages waiting for higher-priority ones to arrive.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example Scenario: Why below example will not work as expected
- You pushed a low-priority message (priority=1)
- You immediately pushed higher ones
- But unless the messages were sitting in the queue while a consumer was attached and idle, they were consumed as they came in

In other words, "Priority works only if there is competition between messages in the queue. RabbitMQ won't reshuffle them on arrival — only when choosing which message to send to a consumer."

To Test Priority Effectively:
Option 1: Publish all first, then start the consumer

```
# In terminal 1: Run publisher
python publisher.py

# Wait a couple seconds

# In terminal 2: Run consumer
python consumer.py
```

Option 2: Add delay between publishing messages (not ideal, but for demo)

You can simulate delay:
```
import time
mq.push_message(... priority=1)
time.sleep(2)
mq.push_message(... priority=10)
```
"""

from mq_connector import MQConnector

mq = MQConnector(broker_url="amqp://guest:guest@localhost:5672/")

# Push messages with different priorities
mq.push_message(
    queue="notify_queue",
    message="Log: User signed in",
    priority=1,
    queue_max_priority=10,
)

mq.push_message(
    queue="notify_queue",
    message="Urgent alert: Disk full",
    priority=10,
    queue_max_priority=10,
)

mq.push_message(
    queue="notify_queue",
    message="New message from user",
    priority=5,
    queue_max_priority=10,
)
