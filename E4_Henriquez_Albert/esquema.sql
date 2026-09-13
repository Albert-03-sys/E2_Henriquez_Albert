-- esquema.sql
-- Fiel al MER del Entregable 1: ESCANEOS, PUERTOS, SERVICIOS, REGLAS, REPORTES

CREATE TABLE IF NOT EXISTS ESCANEOS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    host VARCHAR NOT NULL,
    inicio DATETIME NOT NULL,
    fin DATETIME
);

CREATE TABLE IF NOT EXISTS PUERTOS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    escaneo_id INTEGER NOT NULL,
    numero INTEGER NOT NULL,
    protocolo VARCHAR NOT NULL,
    abierto BOOLEAN NOT NULL,
    FOREIGN KEY(escaneo_id) REFERENCES ESCANEOS(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS SERVICIOS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    puerto_id INTEGER NOT NULL,
    nombre VARCHAR NOT NULL,
    huella VARCHAR,
    version VARCHAR,
    nivel_riesgo VARCHAR,
    FOREIGN KEY(puerto_id) REFERENCES PUERTOS(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS REGLAS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo VARCHAR NOT NULL,
    criterio VARCHAR NOT NULL,
    nivel_riesgo VARCHAR NOT NULL
);

-- DATOS DE PRUEBA (15 registros)
-- 3 Reglas
INSERT INTO REGLAS (tipo, criterio, nivel_riesgo) VALUES ('Puerto', '3306', 'Alto');
INSERT INTO REGLAS (tipo, criterio, nivel_riesgo) VALUES ('Puerto', '22', 'Medio');
INSERT INTO REGLAS (tipo, criterio, nivel_riesgo) VALUES ('Huella', 'Apache', 'Medio');

-- 2 Escaneos
INSERT INTO ESCANEOS (host, inicio, fin) VALUES ('192.168.1.10', '2026-09-10 10:00:00', '2026-09-10 10:05:00');
INSERT INTO ESCANEOS (host, inicio, fin) VALUES ('scanme.nmap.org', '2026-09-11 14:00:00', '2026-09-11 14:02:00');

-- 5 Puertos
INSERT INTO PUERTOS (escaneo_id, numero, protocolo, abierto) VALUES (1, 22, 'TCP', 1);
INSERT INTO PUERTOS (escaneo_id, numero, protocolo, abierto) VALUES (1, 80, 'TCP', 1);
INSERT INTO PUERTOS (escaneo_id, numero, protocolo, abierto) VALUES (1, 443, 'TCP', 0);
INSERT INTO PUERTOS (escaneo_id, numero, protocolo, abierto) VALUES (2, 3306, 'TCP', 1);
INSERT INTO PUERTOS (escaneo_id, numero, protocolo, abierto) VALUES (2, 8080, 'TCP', 1);

-- 5 Servicios (Perfilado)
INSERT INTO SERVICIOS (puerto_id, nombre, huella, version, nivel_riesgo) VALUES (1, 'SSH', 'OpenSSH', '8.2', 'Medio');
INSERT INTO SERVICIOS (puerto_id, nombre, huella, version, nivel_riesgo) VALUES (2, 'HTTP', 'Apache', '2.4', 'Medio');
INSERT INTO SERVICIOS (puerto_id, nombre, huella, version, nivel_riesgo) VALUES (3, 'HTTPS', '-', '-', 'Bajo');
INSERT INTO SERVICIOS (puerto_id, nombre, huella, version, nivel_riesgo) VALUES (4, 'MySQL', 'MySQL', '5.7', 'Alto');
INSERT INTO SERVICIOS (puerto_id, nombre, huella, version, nivel_riesgo) VALUES (5, 'HTTP-Alt', 'Nginx', '1.18', 'Bajo');