import json
import os
from aiokafka import AIOKafkaConsumer
from dotenv import load_dotenv
import logging

load_dotenv()


KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")



class KafkaLogConsumer:
    def __init__(self, topic, insert_log):
        if not KAFKA_BOOTSTRAP_SERVERS:
            raise Exception("empty bootstrap server env variable given")
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )
        self.insert_log = insert_log
        self._running = False

    async def start(self):
        await self.consumer.start()
        self._running = True
        logging.info("Kafka consumer started")

    async def consume_forever(self):
        try:
            async for msg in self.consumer:
                await self.insert_log(msg.value)
                if not self._running:
                    break
        except Exception as e:
            logging.error("Kafka error:", e)
            logging.exception("Kafka consumer crashed")

    async def stop(self):
        self._running = False
        await self.consumer.stop()
        logging.info("Kafka consumer stopped")