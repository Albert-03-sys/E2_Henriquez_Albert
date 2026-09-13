class Servicio:
    def __init__(self, puerto_numero: int, nombre: str, huella: str, version: str):
        # 3. Encapsulación con atributos privados
        self.__puerto_numero = puerto_numero
        self.__nombre = nombre
        self.__huella = huella
        self.version = version
        self.riesgo = "Bajo"

    # Métodos de acceso (Getters) usando decorador property
    @property
    def puerto_numero(self):
        return self.__puerto_numero

    @property
    def nombre(self):
        return self.__nombre

    @property
    def huella(self):
        return self.__huella

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "huella": self.huella,
            "version": self.version,
            "riesgo": self.riesgo
        }