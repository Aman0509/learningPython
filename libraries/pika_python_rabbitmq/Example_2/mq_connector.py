import pika


class MQConnector:
    def __init__(self, broker_url, prefetch_count=1, exchange=""):
        """
        Initialize the MQConnector with the broker URL and prefetch count.

        :param broker_url: URL of the message broker (e.g., RabbitMQ)

        :param prefetch_count: How many unacknowledged messages a consumer can hold at once? For e.g., prefetch_count=1 means RabbitMQ will only deliver one message at a time to the consumer and wait for an ack before sending more

        :param exchange: Name of the exchange to use (defaults to the empty string = default direct exchange). If empty, this exchange compares routing key to queue name instead of binding key. If you publish a message to this exchange with routing key = “order”, the exchange will route this message to the queue with queue name = “order”.

        return: None
        """
        self.exchange = exchange
        self.broker_url = broker_url
        self.prefetch_count = prefetch_count
        self.connection = self.__connect_to_broker()
        self.channel = self.__channel()

    def __connect_to_broker(self):
        """
        Connect to the message broker using the provided URL. Uses blocking connection (synchronous)
        :return: Connection object
        :raises Exception: If the connection fails
        """
        if self.broker_url:
            try:
                connection = pika.BlockingConnection(
                    pika.URLParameters(self.broker_url)
                )
                print("Connected to broker")
                return connection
            except Exception as e:
                print(f"Failed to connect to broker: {e}")
                raise
        return connection

    def __channel(self):
        """
        Create a channel for communication with the broker. Uses blocking connection (synchronous)

        `basic_qos` is used to limit the number of unacknowledged messages that can be sent to a consumer at a time.
        This is useful for controlling the flow of messages and preventing overwhelming the consumer with too many
        messages at once `prefetch_count` is the number of messages to send to consumers before waiting for
        acknowledgments.

        :return: Channel object
        :raises Exception: If channel creation fails
        """
        try:
            channel = self.connection.channel()
            channel.basic_qos(prefetch_count=self.prefetch_count)
            print("Channel created")
            return channel
        except Exception as e:
            print(f"Failed to create channel: {e}")
            raise

    def push_message(
        self, queue, message, priority=0, queue_max_priority=0, header=None
    ):
        """
        Publish a message to the specified queue with optional priority and headers.
        Binds the message to the default exchange (routing_key = queue)

        :param queue: Name of the queue to publish to
        :param message: The message to publish
        :param priority: The priority of the individual message (higher = more important)
        :param queue_max_priority: The maximum priority level the queue will recognize (e.g., 10 means 0–10 allowed)
        :param header: Optional headers to include with the message (default is None)

        :return: None
        :raises Exception: If publishing fails

        Note:
        - Message priority works only if the queue is declared with `x-max-priority`.
        - If you don't declare queue_max_priority, the priority field is ignored entirely.
        - If you send a message with priority=15 but queue_max_priority=10, RabbitMQ will cap it to 10.

        How RabbitMQ uses them:
        - You must declare the queue with x-max-priority.
        - You then publish messages with different priority values.
        - RabbitMQ will deliver higher priority messages first, even if they were published later.

        Example:
        Let's say you want to send notifications, and:
        - Priority 10 = urgent (admin alerts)
        - Priority 5 = normal (user messages)
        - Priority 1 = background (logs)

        ```python
        mq = MQConnector(broker_url='amqp://guest:guest@localhost:5672/')

        mq.push_message(
            queue='notify_queue',
            message='Urgent alert: Disk full',
            priority=10,
            queue_max_priority=10  # enables priority queue
        )

        mq.push_message(
            queue='notify_queue',
            message='New message from user',
            priority=5,
            queue_max_priority=10
        )

        mq.push_message(
            queue='notify_queue',
            message='Log: User signed in',
            priority=1,
            queue_max_priority=10
        )
        ```

        Even if these are pushed in the order shown, RabbitMQ will deliver them in this order:

        - Urgent alert: Disk full (priority 10)
        - New message from user (priority 5)
        - Log: User signed in (priority 1)

        """
        if queue_max_priority > 0:
            self.channel.queue_declare(
                queue=queue,
                durable=True,
                auto_delete=False,
                arguments={"x-max-priority": queue_max_priority},
            )
        else:
            self.channel.queue_declare(queue=queue, durable=True)

        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=queue,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
                priority=priority,
                headers=header,
            ),
        )
        print(f"Message published to {queue}: {message}")

    def consume_queue(self, queue, callback, queue_max_priority=None):
        if queue_max_priority:
            self.channel.queue_declare(
                queue=queue,
                durable=True,
                auto_delete=False,
                arguments={"x-max-priority": queue_max_priority},
            )
        else:
            self.channel.queue_declare(queue=queue, durable=True)

        self.channel.basic_consume(
            queue=queue, on_message_callback=callback, auto_ack=False
        )
        print(f"Started consuming from queue: {queue}")

    def start_consuming(self):
        self.channel.start_consuming()

    def close_consuming(self):
        self.connection.close()
