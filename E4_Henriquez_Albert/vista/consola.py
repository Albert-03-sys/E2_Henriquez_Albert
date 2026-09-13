class VistaConsola:
    @staticmethod
    def mostrar_menu():
        print("\n" + "="*50)
        print("🛡️  ESCÁNER DE PUERTOS Y PERFILES DE SERVICIO")
        print("="*50)
        print("1. Iniciar nuevo escaneo de puertos (Objetivo)")
        print("2. Ver historial de resultados")
        print("3. Exportar datos (JSON crudo en pantalla)")
        print("4. Salir")
        return input("Seleccione una opción: ")

    @staticmethod
    def pedir_datos_escaneo():
        host = input("Ingrese la IP o Host (Ej: 192.168.1.100): ")
        puertos_str = input("Ingrese los puertos separados por coma (Ej: 22,80,3306): ")
        puertos = []
        for p in puertos_str.split(","):
            if p.strip().isdigit():
                puertos.append(int(p.strip()))
        return host, puertos

    @staticmethod
    def mostrar_resultados(escaneo):
        print(f"\n--- Resultados para {escaneo['host']} ---")
        print(f"[{escaneo['inicio']} - {escaneo['fin']}]")
        print(f"{'PUERTO':<10} | {'ESTADO':<10} | {'SERVICIO':<15} | {'RIESGO':<10}")
        print("-" * 55)
        for p in escaneo['puertos']:
            estado = "Abierto" if p['abierto'] else "Cerrado"
            servicio = p['servicio']['nombre'] if p['servicio'] else "N/A"
            riesgo = p['servicio']['riesgo'] if p['servicio'] else "Bajo"
            print(f"{p['numero']:<10} | {estado:<10} | {servicio:<15} | {riesgo:<10}")

    @staticmethod
    def mostrar_mensaje(msg):
        print(f"\n> {msg}")