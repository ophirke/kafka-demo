import json
from kafka import KafkaConsumer

# Consumer
consumer = KafkaConsumer(
    'my-topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')) if v else None
)

for message in consumer:
    print(f"Received message: {message.value}")