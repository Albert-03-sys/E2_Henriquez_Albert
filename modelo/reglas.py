from abc import ABC, abstractmethod

# 1. Clase Abstracta / Interfaz
class ReglaRiesgo(ABC):
    @abstractmethod
    def evaluar(self, servicio) -> str:
        """Método abstracto que deben implementar las clases hijas."""
        pass

# 2. Herencia (Clase hija 1)
class ReglaPorPuerto(ReglaRiesgo):
    def __init__(self, puerto: int, nivel_riesgo: str):
        self.puerto = puerto
        self.nivel_riesgo = nivel_riesgo

    def evaluar(self, servicio) -> str:
        if servicio.puerto_numero == self.puerto:
            return self.nivel_riesgo
        return "Bajo"

# 2. Herencia (Clase hija 2)
class ReglaPorHuella(ReglaRiesgo):
    def __init__(self, huella: str, nivel_riesgo: str):
        self.huella = huella
        self.nivel_riesgo = nivel_riesgo

    def evaluar(self, servicio) -> str:
        if self.huella.lower() in servicio.huella.lower():
            return self.nivel_riesgo
        return "Bajo"