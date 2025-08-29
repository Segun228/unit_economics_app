import json
import os
from aiokafka import AIOKafkaConsumer
from dotenv import load_dotenv
import logging
import asyncio

load_dotenv()


KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")


class KafkaLogConsumer:
    def __init__(self, topic, insert_log):
        if not KAFKA_BOOTSTRAP_SERVERS:
            raise Exception("empty bootstrap server env variable given")
        self.topic = topic
        self.insert_log = insert_log
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )

    async def start(self):
        await self.consumer.start()
        logging.info(f"Kafka consumer started for topic: {self.topic}")

    async def consume_forever(self):
        try:
            while True:
                msg = await self.consumer.getone()
                await self.insert_log(msg.value)
        except asyncio.CancelledError:
            logging.info(f"Kafka consumer task cancelled for topic: {self.topic}")
            raise 
        except Exception as e:
            logging.error(f"Kafka error in topic {self.topic}: {e}")
            logging.exception("Kafka consumer crashed")

    async def stop(self):
        await self.consumer.stop()
        logging.info(f"Kafka consumer stopped for topic: {self.topic}")