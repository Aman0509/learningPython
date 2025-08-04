# [Pika (for RabbitMQ)](https://pika.readthedocs.io/en/stable/intro.html)

Pika is a Python library used to work with RabbitMQ, a popular message broker that implements the Advanced Message Queuing Protocol (AMQP). RabbitMQ allows applications to communicate asynchronously by sending and receiving messages through queues. Pika provides a simple interface to connect to RabbitMQ, publish messages, and consume them.

## Key Features of Pika:

1. **AMQP Support**: Pika supports the AMQP protocol, enabling robust message queuing.
2. **Lightweight**: It is a lightweight library, making it easy to integrate into Python projects.
3. **Flexible**: Pika allows you to create producers (senders) and consumers (receivers) for RabbitMQ.

### Example: Sending and Receiving Messages with Pika

Below is an example of how to use Pika to send and receive messages:

1. **Sending a Message (Producer)**

   ```python
   import pika

   # Establish a connection to RabbitMQ
   connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
   channel = connection.channel()

   # Declare a queue (creates it if it doesn't exist)
   channel.queue_declare(queue='hello')

   # Publish a message to the queue
   channel.basic_publish(exchange='', routing_key='hello', body='Hello, RabbitMQ!')
   print(" [x] Sent 'Hello, RabbitMQ!'")

   # Close the connection
   connection.close()
   ```

2. **Receiving a Message (Consumer)**

   ```python
   import pika

   # Establish a connection to RabbitMQ
   connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
   channel = connection.channel()

   # Declare the same queue (ensures it exists)
   channel.queue_declare(queue='hello')

   # Callback function to process messages
   def callback(ch, method, properties, body):
       print(f" [x] Received {body}")

   # Subscribe to the queue
   channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

   print(' [*] Waiting for messages. To exit press CTRL+C')
   channel.start_consuming()
   ```

### How It Works:

1. **Producer**:

   - Connects to RabbitMQ and declares a queue named hello.
   - Sends a message (Hello, RabbitMQ!) to the queue.

2. **Consumer**:

- Connects to RabbitMQ and declares the same queue (hello).
- Listens for messages on the queue and processes them using the callback function.

**Running the Example:**

- Start RabbitMQ on your system.
- Run the consumer script first to start listening for messages.
- Run the producer script to send a message.

Checkout these examples for more understanding

- [Example 1](Example_1/)
- [Example 1](Example_2/)
