import json
from kafka import KafkaConsumer
from tqdm import tqdm, trange

# Consumer
consumer = KafkaConsumer(
    'my-topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')) if v else None
)

count = 0
for message in consumer:
    count += 1
    if count % 1000 == 0:
        print(count)