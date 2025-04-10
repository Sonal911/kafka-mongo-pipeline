from kafka import KafkaConsumer
from pymongo import MongoClient
import json
import os

bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS", "localhost:9092")


from kafka import KafkaConsumer
from pymongo import MongoClient
import json
import os

def get_kafka_consumer(topic='sensor-output', bootstrap_servers=None):
    return KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers or os.getenv("BOOTSTRAP_SERVERS", "localhost:9092"),
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

def get_mongo_collection(uri="mongodb://admin:adminpassword@mongo:27017/", db_name="sensor_data", coll_name="aggregated_output"):
    client = MongoClient(uri)
    return client[db_name][coll_name]

def consume_and_insert(consumer, collection, limit=None):
    print("Consuming data from Kafka...")
    count = 0
    for message in consumer:
        data = message.value
        print("Inserting:", data)
        collection.insert_one(data)
        count += 1
        if limit and count >= limit:
            break

if __name__ == "__main__":
    consumer = get_kafka_consumer()
    collection = get_mongo_collection()
    consume_and_insert(consumer, collection)