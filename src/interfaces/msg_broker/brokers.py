from abc import ABC, abstractmethod


class IKafkaConsumer(ABC):
    def __init__(self, bootstrap_servers: str, topic: str, group_id: str):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id

    @abstractmethod
    async def consume(self) -> None:
        pass
