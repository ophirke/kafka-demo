import json
from kafka import KafkaProducer

# Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

data = {'name': 'Alice', 'age': 30}

producer.send('my-topic', data)
producer.flush()