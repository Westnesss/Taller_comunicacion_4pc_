# performance_monitor.py
import psutil
import time
from memory_profiler import profile
import json
from mongo_manager import MongoManager
from datetime import datetime

class PerformanceMonitor:
    def __init__(self,id_maquina):
        self.id_maquina=id_maquina
        
    @staticmethod
    def obtener_porcentaje_uso_cpu():
        porcentaje = psutil.cpu_percent(interval=1)
        return porcentaje
    
    @profile
    def my_function():
     a = [1] * (10 ** 6)
     b = [2] * (2 * 10 ** 7)
     del b
     return a
 
    def crear_mensaje(self,tipo,datos):
        fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mensaje={
            "id_maquina":self.id_maquina,
            "tipo":tipo,
            "fecha_hora_actual":fecha_hora_actual,
            **datos
        }
        return mensaje
    
    def enviar_mensaje(self,mqtt_client,topic,tipo,datos,mongo_manager_intance):
        mensaje=self.crear_mensaje(tipo, datos)
        print(mensaje)
        mqtt_client.publish(topic, json.dumps(mensaje))
        mongo_manager_intance.guardar_mensaje(mensaje)
        
        
  
    def monitor_network(self,mqtt_client,topic,mongo_manager_intance,interval=1, duration=10):
        print("Monitoring network performance...")
        end_time = time.time() + duration

        while time.time() < end_time:
            net_stats = psutil.net_io_counters()
            datos ={
                "bytes_enviados": net_stats.bytes_sent,
                "bytes_recibidos": net_stats.bytes_recv
            }
            self.enviar_mensaje(mqtt_client, topic, "monitoreo de red",datos,mongo_manager_intance) 
            time.sleep(interval)

   
    def monitor_cpu(self,mqtt_client,topic,mongo_manager_intance,interval=1, duration=10):
        print("Monitoring CPU performance...")
        end_time = time.time() + duration

        while time.time() < end_time:
            cpu_percent = psutil.cpu_percent(interval=interval)
            datos = {
                "porcentaje": cpu_percent  
            }
            f"Uso de CPU: {cpu_percent}%"
            self.enviar_mensaje(mqtt_client,topic,"Uso CPU",datos,mongo_manager_intance)
            time.sleep(interval)
