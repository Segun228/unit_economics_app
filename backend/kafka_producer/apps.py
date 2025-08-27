from django.apps import AppConfig


class KafkaProducerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kafka_producer'
