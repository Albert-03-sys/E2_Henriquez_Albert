import time
import random
from modelo.escaneo import Escaneo
from modelo.puerto import Puerto
from modelo.servicio import Servicio
from modelo.reglas import ReglaPorPuerto, ReglaPorHuella
from modelo.excepciones import PuertoInvalidoError
from datos.dao import DAO
from vista.gui import VistaPrincipal

class ControladorEscaneo:
    def __init__(self):
        self.dao = DAO()
        self.vista = VistaPrincipal(self)

    def iniciar_app(self):
        self.vista.mainloop()

    def _cargar_reglas_desde_bd(self):
        reglas_bd = self.dao.obtener_reglas()
        reglas_modelo = []
        for r in reglas_bd:
            if r['tipo'] == 'Puerto':
                reglas_modelo.append(ReglaPorPuerto(int(r['criterio']), r['nivel_riesgo']))
            else:
                reglas_modelo.append(ReglaPorHuella(r['criterio'], r['nivel_riesgo']))
        return reglas_modelo

    def ejecutar_escaneo_gui(self, host, puertos_num):
        nuevo_escaneo = Escaneo(0, host)
        reglas_activas = self._cargar_reglas_desde_bd()
        
        time.sleep(0.5)

        for num in puertos_num:
            try:
                puerto = Puerto(num, "TCP", abierto=random.choice([True, False]))
                if puerto.abierto:
                    diccionario_servicios = {22: ("SSH", "OpenSSH", "8.2"), 80: ("HTTP", "Apache", "2.4"), 3306: ("MySQL", "MySQL", "5.7")}
                    s_data = diccionario_servicios.get(num, ("Desconocido", "Unknown", "1.0"))
                    servicio = Servicio(num, s_data[0], s_data[1], s_data[2])
                    
                    for regla in reglas_activas:
                        nivel = regla.evaluar(servicio)
                        if nivel != "Bajo":
                            servicio.riesgo = nivel
                    puerto.asignar_servicio(servicio)
                nuevo_escaneo.agregar_puerto(puerto)
            except PuertoInvalidoError:
                pass

        nuevo_escaneo.finalizar()
        try:
            self.dao.guardar_escaneo_completo(nuevo_escaneo)
            return True, "Escaneo finalizado y guardado en BD."
        except Exception as e:
            return False, str(e)

    # Operaciones delegadas al DAO
    def obtener_historial(self): return self.dao.obtener_historial_escaneos()
    def obtener_datos_graficas(self): return {'riesgos': self.dao.obtener_datos_riesgos(), 'estados': self.dao.obtener_datos_estados()}
    def obtener_reglas(self): return self.dao.obtener_reglas()
    def crear_regla(self, tipo, crit, riesg): self.dao.crear_regla(tipo, crit, riesg)
    def eliminar_regla(self, id_r): self.dao.eliminar_regla(id_r)
    def eliminar_escaneo(self, id_e): self.dao.eliminar_escaneo(id_e)