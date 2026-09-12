import time
import random
from modelo.escaneo import Escaneo
from modelo.puerto import Puerto
from modelo.servicio import Servicio
from modelo.reglas import ReglaPorPuerto, ReglaPorHuella
from modelo.excepciones import PuertoInvalidoError
from datos.repositorio import RepositorioJSON
from vista.consola import VistaConsola

class ControladorEscaneo:
    def __init__(self):
        self.repo = RepositorioJSON()
        self.vista = VistaConsola()
        self.datos = self.repo.cargar_datos()
        
        # Cargamos reglas en memoria
        self.reglas = [
            ReglaPorPuerto(3306, "Alto"),
            ReglaPorPuerto(22, "Medio"),
            ReglaPorHuella("Apache", "Medio")
        ]

    def iniciar_app(self):
        while True:
            opcion = self.vista.mostrar_menu()
            if opcion == '1':
                self.ejecutar_escaneo()
            elif opcion == '2':
                self.ver_resultados()
            elif opcion == '3':
                self.exportar_datos()
            elif opcion == '4':
                self.vista.mostrar_mensaje("Saliendo del sistema...")
                break
            else:
                self.vista.mostrar_mensaje("Opción no válida.")

    def ejecutar_escaneo(self):
        host, puertos_num = self.vista.pedir_datos_escaneo()
        id_escaneo = len(self.datos.get('escaneos', [])) + 1
        nuevo_escaneo = Escaneo(id_escaneo, host)

        self.vista.mostrar_mensaje("Ejecutando motor de escaneo (Simulado)...")
        time.sleep(1)

        for num in puertos_num:
            try:
                # Instanciamos puerto (puede arrojar PuertoInvalidoError)
                puerto = Puerto(num, "TCP", abierto=random.choice([True, False]))
                
                if puerto.abierto:
                    # Simulamos el perfilado de servicios basados en puertos comunes
                    diccionario_servicios = {
                        22: ("SSH", "OpenSSH 8.2", "8.2"),
                        80: ("HTTP", "Apache/2.4", "2.4"),
                        3306: ("MySQL", "MySQL 5.7", "5.7")
                    }
                    s_data = diccionario_servicios.get(num, ("Desconocido", "Unknown", "1.0"))
                    servicio = Servicio(num, s_data[0], s_data[1], s_data[2])
                    
                    # 5. Polimorfismo: Llamamos a 'evaluar' de manera uniforme sin importar 
                    # si la regla es ReglaPorPuerto o ReglaPorHuella.
                    for regla in self.reglas:
                        nivel = regla.evaluar(servicio)
                        if nivel != "Bajo":
                            servicio.riesgo = nivel
                    
                    puerto.asignar_servicio(servicio)
                
                nuevo_escaneo.agregar_puerto(puerto)
            except PuertoInvalidoError as e:
                self.vista.mostrar_mensaje(f"Ignorando puerto: {e}")

        nuevo_escaneo.finalizar()
        self.datos['escaneos'].append(nuevo_escaneo.to_dict())
        self.repo.guardar_datos(self.datos)
        
        self.vista.mostrar_mensaje("Escaneo completado. Resultados:")
        self.vista.mostrar_resultados(nuevo_escaneo.to_dict())

    def ver_resultados(self):
        escaneos = self.datos.get('escaneos', [])
        if not escaneos:
            self.vista.mostrar_mensaje("No hay escaneos históricos.")
            return
        for e in escaneos:
            self.vista.mostrar_resultados(e)

    def exportar_datos(self):
        self.vista.mostrar_mensaje("Exportación de los datos en formato crudo (JSON):")
        import json
        print(json.dumps(self.datos, indent=2))