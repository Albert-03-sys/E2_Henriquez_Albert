import sqlite3
import os

class DAO:
    def __init__(self, db_name="datos/db_ciberseguridad.sqlite"):
        self.db_name = db_name
        self._inicializar_bd()

    def _conectar(self):
        try:
            conn = sqlite3.connect(self.db_name)
            conn.row_factory = sqlite3.Row
            # Activar foreign keys en SQLite
            conn.execute("PRAGMA foreign_keys = ON")
            return conn
        except sqlite3.Error as e:
            raise Exception(f"Error de conexión a la base de datos: Compruebe los permisos locales.")

    def _inicializar_bd(self):
        if not os.path.exists(self.db_name):
            try:
                with self._conectar() as conn:
                    with open("esquema.sql", "r", encoding="utf-8") as f:
                        conn.executescript(f.read())
            except Exception as e:
                print(f"Error al inicializar BD: {e}")

    # ================= CRUD REGLAS (Entidad 1) =================
    def crear_regla(self, tipo, criterio, riesgo):
        # 1. Consulta Parametrizada (Prevención Inyección SQL)
        sql = "INSERT INTO REGLAS (tipo, criterio, nivel_riesgo) VALUES (?, ?, ?)"
        try:
            with self._conectar() as conn:
                conn.execute(sql, (tipo, criterio, riesgo))
                conn.commit()
        except sqlite3.Error:
            raise Exception("No se pudo crear la regla.")

    def obtener_reglas(self):
        sql = "SELECT * FROM REGLAS"
        with self._conectar() as conn:
            return [dict(row) for row in conn.execute(sql).fetchall()]

    def eliminar_regla(self, id_regla):
        sql = "DELETE FROM REGLAS WHERE id = ?"
        with self._conectar() as conn:
            conn.execute(sql, (id_regla,))
            conn.commit()

    # ================= CRUD ESCANEOS (Entidad 2) =================
    def guardar_escaneo_completo(self, escaneo):
        sql_escaneo = "INSERT INTO ESCANEOS (host, inicio, fin) VALUES (?, ?, ?)"
        sql_puerto = "INSERT INTO PUERTOS (escaneo_id, numero, protocolo, abierto) VALUES (?, ?, ?, ?)"
        sql_servicio = "INSERT INTO SERVICIOS (puerto_id, nombre, huella, version, nivel_riesgo) VALUES (?, ?, ?, ?, ?)"
        
        try:
            with self._conectar() as conn:
                cursor = conn.cursor()
                cursor.execute(sql_escaneo, (escaneo.host, escaneo.inicio, escaneo.fin))
                escaneo_id = cursor.lastrowid
                
                for p in escaneo.puertos:
                    cursor.execute(sql_puerto, (escaneo_id, p.numero, p.protocolo, p.abierto))
                    puerto_id = cursor.lastrowid
                    if p.servicio:
                        cursor.execute(sql_servicio, (puerto_id, p.servicio.nombre, p.servicio.huella, p.servicio.version, p.servicio.riesgo))
                conn.commit()
        except sqlite3.Error:
            raise Exception("Error al guardar el escaneo en la base de datos.")

    def eliminar_escaneo(self, id_escaneo):
        # El ON DELETE CASCADE en SQLite borra automáticamente puertos y servicios
        sql = "DELETE FROM ESCANEOS WHERE id = ?"
        with self._conectar() as conn:
            conn.execute(sql, (id_escaneo,))
            conn.commit()

    # ================= CONSULTAS DE NEGOCIO Y GRÁFICAS =================
    
    def obtener_historial_escaneos(self):
        # 2. Consulta con JOIN y Función de Agregación (COUNT y GROUP BY)
        sql = """
            SELECT e.id, e.host, e.inicio, COUNT(p.id) as total_puertos 
            FROM ESCANEOS e 
            LEFT JOIN PUERTOS p ON e.id = p.escaneo_id 
            GROUP BY e.id
        """
        with self._conectar() as conn:
            return [dict(row) for row in conn.execute(sql).fetchall()]

    def obtener_datos_riesgos(self):
        # 3. Consulta con JOIN y Función de Agregación (Gráfica 1)
        sql = """
            SELECT s.nivel_riesgo, COUNT(*) as total 
            FROM SERVICIOS s 
            JOIN PUERTOS p ON s.puerto_id = p.id 
            WHERE p.abierto = 1 
            GROUP BY s.nivel_riesgo
        """
        with self._conectar() as conn:
            return {row['nivel_riesgo']: row['total'] for row in conn.execute(sql).fetchall()}

    def obtener_datos_estados(self):
        # 4. Consulta con Función de Agregación (Gráfica 2)
        sql = "SELECT abierto, COUNT(*) as total FROM PUERTOS GROUP BY abierto"
        with self._conectar() as conn:
            resultados = conn.execute(sql).fetchall()
            return {'Abiertos': sum(r['total'] for r in resultados if r['abierto'] == 1),
                    'Cerrados': sum(r['total'] for r in resultados if r['abierto'] == 0)}