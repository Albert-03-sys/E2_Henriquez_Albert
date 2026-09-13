# Escáner de Puertos y Perfiles de Servicio (TECI) 🛡️

Aplicación de escritorio bajo arquitectura MVC para la automatización de escaneos de puertos y clasificación de riesgos, desarrollada en Python y SQLite.

## Requisitos de Sistema
* Python 3.10 o superior.
* Librerías: `matplotlib`
* Sistema Operativo: Multiplataforma (Probado en Windows 11 - Dell Inspiron).

## Instalación
1. Clonar el repositorio.
2. Instalar dependencias ejecutando: `pip install matplotlib`

## Configuración de Base de Datos
La aplicación utiliza SQLite. No requiere instalación de un motor de base de datos pesado.
Al ejecutar la aplicación por primera vez, el sistema leerá automáticamente el archivo `esquema.sql` y creará el archivo `datos/db_ciberseguridad.sqlite` inyectando 15 registros de prueba predeterminados.

## Ejecución
Desde la terminal en la raíz del proyecto, ejecutar:
`python main.py`