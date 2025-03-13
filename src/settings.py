import os

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    POSTGRES_URI: str = os.environ.get('POSTGRES_URI')
    BROKER: str = os.environ.get('CELERY_BROKER_URL')
    BACKEND: str = os.environ.get('CELERY_RESULT_BACKEND')

    KAFKA_URL: str = "kafka:29092"
    GROUP_ID: str = "test"
    KAFKA_TOPIC: str = "test"
    ORACLE_URI: str = os.environ.get('ORACLE_CONNECTION')
    NEW_ORACLE_URI: str = os.environ.get('NEW_ORACLE_URI')
    MONGO: str = "mongodb://root:root@mongo:27017/?authSource=admin"
    KAFKA_BOOTSTRAP_SERVERS = "kafka:29092"

settings = Settings()


from dataclasses import dataclass

@dataclass
class KafkaConfig:
    bootstrap_servers: str
    topic: str
    group_id: str