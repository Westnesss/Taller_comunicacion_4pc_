# main.py
import mongo_manager
import mqtt_manager
import performance_monitor
from correos import AlertasCorreo
from uuid import getnode
import json
import time

def obtener_direccion_mac():
    mac_address = ':'.join(['{:02x}'.format((getnode() >> elements) & 0xff) for elements in range(2, 7)][::-1])
    return mac_address

class Main:
    @staticmethod
    def ejecutar():
        # Configuración global
        #host = "broker.hivemq.com"
        #port = 1883
        #topic = "Bad_boys"
        
        #configuracion para 4 computadoras
        configuraciones = [
            {"host": "broker.hiveq.com", "port": 1883, "topic": "Bad_boys"},
            {"host": "broker.hiveq.com", "port": 1883, "topic": "computadora2"},
            {"host": "broker.hiveq.com", "port": 1883, "topic": "computadora3"},
            {"host": "broker.hiveq.com", "port": 1883, "topic": "computadora4"},
        ]
        for configuracion in configuraciones:
            host = configuracion["host"]
            port = configuracion["port"]
            topic = configuracion["topic"]
        # Inicialización de las clases
            mongo_manager_intance = mongo_manager.MongoManager()
            mqtt_managerr = mqtt_manager.MqttManager(host, port, topic)
            try:
               mqtt_managerr.conectar()
            except Exception as e:
                print(f"Error al conectar al servidor MQTT ({host}:{port}): {e}")
                continue  # Pasa a la siguiente configuración si hay un error de conexión
        
        # Inicialización de las clases configuracion global
        #mongo_manager_intance = mongo_manager.MongoManager()
        #mqtt_managerr = mqtt_manager.MqttManager(host, port, topic)    


        # Conexión al servidor MQTT y suscripción al tema
        #mqtt_managerr.conectar()
        mqtt_managerr.suscribirse()
        mqtt_managerr.iniciar_loop()

        # Ejecución de funciones de recopilación de información
        porcentaje_uso_cpu = performance_monitor.PerformanceMonitor.obtener_porcentaje_uso_cpu()
        print(f"Porcentaje de uso de CPU: {porcentaje_uso_cpu}%")

        AlertasCorreo.enviar_alerta_porcentaje_cpu(porcentaje_uso_cpu)

        # Enviar dirección MAC una única vez
        mac_address = obtener_direccion_mac()
        mensaje = {
            "tipo": "direccion MAC",
            "direccion": mac_address
        }
        print(mensaje)
        mqtt_managerr.publicar_mensaje(mensaje)

        mongo_manager_intance.guardar_mensaje(mensaje)

        performance_monitor.PerformanceMonitor.my_function()
        
        id_maquina = mac_address
        performance_monitor_instance = performance_monitor.PerformanceMonitor(id_maquina)
        performance_monitor_instance.monitor_network(mqtt_managerr.mqtt_client, topic, mongo_manager_intance)
        performance_monitor_instance.monitor_cpu(mqtt_managerr.mqtt_client, topic, mongo_manager_intance)

        #performance_monitor.PerformanceMonitor.monitor_network(mqtt_managerr.mqtt_client, topic,mongo_manager_intance)

        #performance_monitor.PerformanceMonitor.monitor_cpu(mqtt_managerr.mqtt_client, topic,mongo_manager_intance)

        # Espera a que las publicaciones MQTT se completen antes de salir
        mqtt_managerr.detener_loop()

if __name__ == "__main__":
    Main.ejecutar()
