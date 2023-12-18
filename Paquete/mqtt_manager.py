# mqtt_manager.py
import paho.mqtt.client as mqtt
import json

class MqttManager:
    def __init__(self, host, port, topic):
        self.mqtt_client = mqtt.Client()
        self.host = host
        self.port = port
        self.topic = topic

    def conectar(self):
        self.mqtt_client.connect(self.host, self.port, 60)

    def suscribirse(self):
        self.mqtt_client.subscribe(self.topic)

    def iniciar_loop(self):
        self.mqtt_client.loop_start()

    def detener_loop(self):
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()

    def publicar_mensaje(self, mensaje):
        self.mqtt_client.publish(self.topic, json.dumps(mensaje))
