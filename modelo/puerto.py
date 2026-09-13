from .excepciones import PuertoInvalidoError
from .servicio import Servicio

class Puerto:
    def __init__(self, numero: int, protocolo: str = "TCP", abierto: bool = False):
        if not (1 <= numero <= 65535):
            raise PuertoInvalidoError(f"El puerto {numero} es inválido. Debe estar entre 1 y 65535.")
        
        self.__numero = numero
        self.protocolo = protocolo
        self.abierto = abierto
        self.servicio = None

    @property
    def numero(self):
        return self.__numero

    def asignar_servicio(self, servicio: Servicio):
        self.servicio = servicio

    def to_dict(self):
        return {
            "numero": self.numero,
            "protocolo": self.protocolo,
            "abierto": self.abierto,
            "servicio": self.servicio.to_dict() if self.servicio else None
        }