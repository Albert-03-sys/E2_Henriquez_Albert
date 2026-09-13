import time
import random
from modelo.escaneo import Escaneo
from modelo.puerto import Puerto
from modelo.servicio import Servicio
from modelo.reglas import ReglaPorPuerto, ReglaPorHuella
from modelo.excepciones import PuertoInvalidoError
from datos.repositorio import RepositorioJSON
from vista.gui import VistaPrincipal # <-- Ahora importamos la GUI

class ControladorEscaneo:
    def __init__(self):
        self.repo = RepositorioJSON()
        self.datos = self.repo.cargar_datos()
        
        # Las reglas de negocio permanecen intactas (Demostración de MVC)
        self.reglas = [
            ReglaPorPuerto(3306, "Alto"),
            ReglaPorPuerto(22, "Medio"),
            ReglaPorHuella("Apache", "Medio")
        ]
        
        # Inicializamos la vista pasándole este controlador
        self.vista = VistaPrincipal(self)

    def iniciar_app(self):
        # Inicia el bucle de eventos de Tkinter
        self.vista.mainloop()

    # Nuevo método adaptado para recibir datos de la GUI directamente
    def ejecutar_escaneo_gui(self, host, puertos_num):
        id_escaneo = len(self.datos.get('escaneos', [])) + 1
        nuevo_escaneo = Escaneo(id_escaneo, host)

        # Simulamos latencia de red
        time.sleep(0.5)

        for num in puertos_num:
            try:
                puerto = Puerto(num, "TCP", abierto=random.choice([True, False]))
                
                if puerto.abierto:
                    diccionario_servicios = {
                        22: ("SSH", "OpenSSH 8.2", "8.2"),
                        80: ("HTTP", "Apache/2.4", "2.4"),
                        3306: ("MySQL", "MySQL 5.7", "5.7")
                    }
                    s_data = diccionario_servicios.get(num, ("Desconocido", "Unknown", "1.0"))
                    servicio = Servicio(num, s_data[0], s_data[1], s_data[2])
                    
                    for regla in self.reglas:
                        nivel = regla.evaluar(servicio)
                        if nivel != "Bajo":
                            servicio.riesgo = nivel
                    
                    puerto.asignar_servicio(servicio)
                
                nuevo_escaneo.agregar_puerto(puerto)
            except PuertoInvalidoError:
                pass # Silenciamos el error para no colgar la UI

        nuevo_escaneo.finalizar()
        self.datos['escaneos'].append(nuevo_escaneo.to_dict())
        self.repo.guardar_datos(self.datos)

    def obtener_historial(self):
        return self.datos.get('escaneos', [])

    def obtener_datos_graficas(self):
        # Agrega datos del modelo para pasarlos a Matplotlib en la Vista
        escaneos = self.obtener_historial()
        resumen = {
            'riesgos': {'Bajo': 0, 'Medio': 0, 'Alto': 0},
            'estados': {'Abiertos': 0, 'Cerrados': 0}
        }
        
        for escaneo in escaneos:
            for p in escaneo['puertos']:
                if p['abierto']:
                    resumen['estados']['Abiertos'] += 1
                    if p['servicio']:
                        riesgo = p['servicio']['riesgo']
                        resumen['riesgos'][riesgo] = resumen['riesgos'].get(riesgo, 0) + 1
                else:
                    resumen['estados']['Cerrados'] += 1
                    
        return resumen