from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')
for i in range(100000):
    message = f"Message number {i}"
    producer.send('my-topic', message.encode('utf-8'))
producer.flush()