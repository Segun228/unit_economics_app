from kafka import KafkaProducer
from fastapi import HTTPException
from produce_schema import ProduceMessage
import json
import logging

KAFKA_BROKER_URL = "localhost:29092"

KAFKA_TOPIC = 'logs_topic'

PRODUCER_CLIENT_ID = 'backend_producer'

def serializer(message):
    return json.dumps(message).encode()

SERIALIZER = serializer


producer = KafkaProducer(
    bootstrap_servers = KAFKA_BROKER_URL,
    value_serializer = serializer,
    client_id = PRODUCER_CLIENT_ID
)


def produce_kafka_message(messageRequest: ProduceMessage):
    try:
        producer.send(
            KAFKA_TOPIC,
            json.dumps({
                "message": messageRequest.message
            })
        )
        producer.flush()
    except Exception as error:
        logging.error(error)
        raise HTTPException(status_code=500, detail="Unable to send message")