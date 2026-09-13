import json
import os

class RepositorioJSON:
    def __init__(self, archivo="datos/db_escaneos.json"):
        self.archivo = archivo
        self._asegurar_directorio()

    def _asegurar_directorio(self):
        os.makedirs(os.path.dirname(self.archivo), exist_ok=True)
        if not os.path.exists(self.archivo):
            self.guardar_datos({"escaneos": []})

    def cargar_datos(self):
        # 4. Manejo de excepciones en operaciones de riesgo (lectura de archivos)
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[!] Error al leer BD ({e}). Creando estructura limpia...")
            return {"escaneos": []}

    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4)
        except IOError as e:
            print(f"[!] Error crítico de E/S al guardar los datos: {e}")