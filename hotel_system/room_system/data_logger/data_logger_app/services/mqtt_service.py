import threading
import time
import logging
from paho.mqtt.client import Client
from django.db.models.signals import Signal

logger = logging.getLogger(__name__)

mqtt_message_received = Signal()

class MQTTService:
    def __init__(self, broker, port, topic, username=None, password=None):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.username = username
        self.password = password
        self.client = Client()
        self.running = False
        self.thread = None

        # Set username and password if provided
        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)

        # Attach callbacks
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info('Connected to MQTT Broker')
            self.client.subscribe(self.topic)
            logger.info(f'Subscribed to topic: {self.topic}')
        else:
            logger.error(f'Failed to connect to MQTT Broker, return code {rc}')

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            logger.warning('Unexpected disconnection, attempting to reconnect...')
            self.reconnect()

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode('utf-8')
        logger.info(f'Message received on topic {msg.topic}: {payload}')
        mqtt_message_received.send(sender=self.__class__, topic=msg.topic, message=payload)

    def reconnect(self):
        while self.running:
            try:
                logger.info('Attempting to reconnect...')
                self.client.reconnect()
                break
            except Exception as e:
                logger.error(f'Reconnect failed: {e}')
                time.sleep(5)

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def run(self):
        while self.running:
            try:
                logger.info('Starting MQTT client...')
                self.client.connect(self.broker, self.port, keepalive=60)
                self.client.loop_forever()
            except Exception as e:
                logger.error(f'MQTT client encountered an error: {e}')
                time.sleep(5)  # Wait before retrying

    def stop(self):
        logger.info('Stopping MQTT client...')
        self.running = False
        self.client.disconnect()
        if self.thread:
            self.thread.join()
        logger.info('MQTT client stopped')
