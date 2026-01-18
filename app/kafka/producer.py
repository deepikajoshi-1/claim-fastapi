"""
In Kafka, topics are created using Kafka CLI where we define how many partitions and replicas we want.
 In our FastAPI application, we only configure a Kafka producer to connect to the Kafka cluster using a bootstrap server. 
 When an API request is processed, we convert our Python data into JSON and publish it to the required topic. 
 Kafka then takes care of storing the message and routing it to the correct partition. 
 Our application just produces the event and doesn’t manage partitions or storage
 
"""

from kafka import KafkaProducer
import json

# Takes a Python dictionary. Converts it to JSON string → json.dumps(v)
# Converts JSON string to bytes → .encode("utf-8")
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def publish_event(topic: str, event: dict, claim_id: str):
    """
    Publishes an event to the specified Kafka topic.

    Args:
        topic (str): The Kafka topic to publish to.
        event (dict): The event data to publish.
        claim_id (str): The claim ID to use as the message key.
    """
    producer.send(topic,key=str(claim_id).encode(),value=event)
    producer.flush()
    