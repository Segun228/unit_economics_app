from kafka import KafkaProducer
import json
import logging
import uuid
import json
import logging
from datetime import datetime, timezone


KAFKA_BROKER_URL = "localhost:29092"
KAFKA_TOPIC = "logs_topic"
PRODUCER_CLIENT_ID = "django_backend_producer"


producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda m: json.dumps(m).encode("utf-8"),
    client_id=PRODUCER_CLIENT_ID,
)


def build_log_message(
    user_id,
    is_authenticated,
    telegram_id,
    action,
    response_code = 200,
    request_method = "GET",
    request_body=None,
    platform = "backend",
    level="INFO",
    source="backend",
    env="prod",
    timestamp=None
):
    message = {
        "timestamp": timestamp or datetime.now(timezone.utc).isoformat(),
        "trace_id": str(uuid.uuid4()),
        "user_id": user_id,
        "is_authenticated": is_authenticated,
        "telegram_id": telegram_id,
        "platform": platform,
        "action": action,
        "request_method": request_method,
        "request_body": request_body,
        "response_code": response_code,
        "level": level,
        "event_type": action,
        "source": source,
        "env": env,
        "message": f"User {user_id} performed {action}"
    }

    return send_to_kafka(message)


def send_to_kafka(data):
    try:
        messages = []

        if isinstance(data, list):
            for el in data:
                if hasattr(el, "dict"):
                    el = el.dict()
                serialized = json.dumps(el).encode("utf-8")
                messages.append(el)
                producer.send(KAFKA_TOPIC, value=serialized)
        else:
            if hasattr(data, "dict"):
                data = data.dict()
            serialized = json.dumps(data).encode("utf-8")
            messages.append(data)
            producer.send(KAFKA_TOPIC, value=serialized)

        producer.flush()

        return {
            "status": "ok",
            "code": 200,
            "messages_sent": len(messages),
            "sample": messages[0] if messages else None,
        }

    except Exception as e:
        logging.error(f"[Kafka] Ошибка отправки: {e}")
        raise RuntimeError("Kafka message send failed")