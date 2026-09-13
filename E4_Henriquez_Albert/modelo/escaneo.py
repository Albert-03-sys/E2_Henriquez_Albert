from datetime import datetime
from .puerto import Puerto

class Escaneo:
    def __init__(self, id_escaneo: int, host: str):
        self.id = id_escaneo
        self.host = host
        self.inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.fin = None
        self.puertos = []

    def agregar_puerto(self, puerto: Puerto):
        self.puertos.append(puerto)

    def finalizar(self):
        self.fin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "id": self.id,
            "host": self.host,
            "inicio": self.inicio,
            "fin": self.fin,
            "puertos": [p.to_dict() for p in self.puertos]
        }