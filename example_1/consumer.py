from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'my-topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
  # Start reading from the beginning of the topic
    group_id='my-group'  # Consumer group ID
)

for message in consumer:
    print(f"Received message: {message.value.decode('utf-8')}")