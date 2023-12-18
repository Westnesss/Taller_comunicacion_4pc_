# mongo_manager.py
from pymongo import MongoClient
import json
import time

class MongoManager:
    def __init__(self):
        self.mongo_client = MongoClient("mongodb://localhost:27017/")
        self.db = self.mongo_client["rendimiento"]
        self.collection = self.db["mensajes"]

    def guardar_mensaje(self, mensaje):
        mensaje_json = json.dumps(mensaje)
        self.collection.insert_one({"mensaje": mensaje_json, "timestamp": time.time()})
