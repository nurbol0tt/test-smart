import asyncio
import json
import logging

from aiokafka import (
    AIOKafkaConsumer,
)

from src.interfaces.msg_broker.brokers import IKafkaConsumer


# class KafkaConsumer(IKafkaConsumer):
#     def __init__(
#             self,
#             bootstrap_servers: str,
#             topic: str,
#             group_id: str
#     ):
#         self.bootstrap_servers = bootstrap_servers
#         self.topic = topic
#         self.group_id = group_id
#         self.consumer = None
#
#     async def start(self):
#         self.consumer = AIOKafkaConsumer(
#             self.topic,
#             bootstrap_servers=self.bootstrap_servers,
#             group_id=self.group_id,
#             auto_offset_reset='earliest',
#             enable_auto_commit=True,
#             retry_backoff_ms=1000
#         )
#         await self.consumer.start()
#
#     async def consume_messages(self):
#         try:
#             async for message in self.consumer:
#                 value = message.value.decode('utf-8')
#                 try:
#                     json_data = json.loads(value)
#                     logging.info(f"Received from kafka: {json_data}")
#                     return await json_data
#                 except json.JSONDecodeError as e:
#                     logging.error(f"JSON Decode Error: {e}")
#         finally:
#             await self.consumer.stop()

class KafkaConsumerService(IKafkaConsumer):
    def __init__(self, bootstrap_servers: str, topic: str, group_id: str):
        super().__init__(bootstrap_servers, topic, group_id)
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )
        self._task = None

    async def consume(self) -> None:
        print("KafkaConsumerService: Starting consumer...")
        try:
            await self.consumer.start()
            print("KafkaConsumerService: Consumer started.")
            async for msg in self.consumer:
                print(f"KafkaConsumerService: Raw message: {msg}")
                if msg.value:
                    try:
                        print(f"KafkaConsumerService: Decoded message: {msg.value.decode()}")
                    except Exception as e:
                        print(f"KafkaConsumerService: Decode error: {e}")
        except Exception as e:
            print(f"KafkaConsumerService: Error in consumer: {e}")
        finally:
            await self.consumer.stop()
            print("KafkaConsumerService: Consumer stopped.")

    def start_background_task(self):
        self._task = asyncio.create_task(self.consume())

    async def stop_background_task(self):
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                print("KafkaConsumerService: Consumer task cancelled.")
