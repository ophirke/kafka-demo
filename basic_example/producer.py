import json
from kafka import KafkaProducer
from multiprocessing import Pool

# Producer
def produce_data(elems):
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    for i in range(elems):
        hash_i = str(hash(i)) + '0' * (16 - len(str(hash(i))))
        name = hash_i
        age = i % 40 + 10
        data = {'name': name, 'age': age}
        producer.send('my-topic', data)
    producer.flush()

if __name__ == '__main__':
    threads = 8
    prod = 100
    total = 1000000
    per_prod_list = [total // prod] * prod
    per_prod_list[-1] += total % prod
    with Pool(threads) as p:
        p.map(produce_data, per_prod_list)