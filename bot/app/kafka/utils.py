from kafka import KafkaProducer
import json
import logging
import uuid
import json
import logging
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

load_dotenv()

KAFKA_BROKER_DOCKER = os.getenv("KAFKA_BROKER_DOCKER")
KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
PRODUCER_CLIENT_ID = os.getenv("PRODUCER_CLIENT_ID")

if not KAFKA_BROKER_DOCKER:
    raise RuntimeError("KAFKA_BROKER_DOCKER not set in environment")

def ensure_topic_exists():
    admin_client = KafkaAdminClient(
        bootstrap_servers=KAFKA_BROKER_DOCKER,
        client_id="admin_client"
    )

    topic_list = [NewTopic(
        name=KAFKA_TOPIC,
        num_partitions=1,
        replication_factor=1
    )]

    try:
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
        print(f"Topic '{KAFKA_TOPIC}' created")
    except TopicAlreadyExistsError:
        print(f"Topic '{KAFKA_TOPIC}' already exists")
    finally:
        admin_client.close()

_producer = None

def get_producer():
    global _producer
    if _producer is None:
        try:
            from kafka import KafkaProducer
            import json
            _producer = KafkaProducer(
                bootstrap_servers=KAFKA_BROKER_DOCKER,
                client_id=PRODUCER_CLIENT_ID,
            )
        except Exception as e:
            logging.warning(f"Kafka producer not available: {e}")
            _producer = None
    return _producer


def build_log_message(
    telegram_id,
    action,
    source,
    payload = None,
    platform = "bot",
    level="INFO",
    env="prod",
    timestamp=None
):
    message = {
        "timestamp": timestamp or datetime.now(timezone.utc).isoformat(),
        "trace_id": str(uuid.uuid4()),
        "telegram_id": telegram_id,
        "platform": platform,
        "action": action,
        "level": level,
        "event_type": action,
        "source": source,
        "env": env,
        "message": f"User {telegram_id} performed {action}"
    }

    return send_to_kafka(message)

def serialize_bytes(obj):
    if isinstance(obj, bytes):
        return obj.decode("utf-8", errors="replace")
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

def send_to_kafka(data):
    producer = get_producer()
    if producer is None:
        logging.info(f"Kafka not available, skipping log: {data}")
        return {"status": "skipped", "messages_sent": 0}

    try:
        messages = []

        if isinstance(data, list):
            for el in data:
                if hasattr(el, "dict"):
                    el = el.dict()
                serialized = json.dumps(el, default=serialize_bytes).encode("utf-8")
                messages.append(el)
                producer.send(KAFKA_TOPIC, value=serialized)
        else:
            if hasattr(data, "dict"):
                data = data.dict()
            serialized = json.dumps(data, default=serialize_bytes).encode("utf-8")
            messages.append(data)
            producer.send(KAFKA_TOPIC, value=serialized)

        producer.flush()
        res = {
            "status": "ok",
            "code": 200,
            "messages_sent": len(messages),
            "sample": messages[0] if messages else None,
        }
        logging.debug(res)
        logging.info("Logged to Kafka successfully!")
        return res

    except Exception as e:
        logging.exception(f"[Kafka] Ошибка отправки: {e}")
        return {"status": "failed", "error": str(e)}