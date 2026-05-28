-- 1. CREACIÓN DE LA NUEVA BASE DE DATOS DEFINITIVA
CREATE DATABASE IF NOT EXISTS fibra_cba_db;
USE fibra_cba_db;

-- 2. TABLAS INDEPENDIENTES (Catálogos y Datos Fijos)
CREATE TABLE IF NOT EXISTS servicios (
    id_servicio INT AUTO_INCREMENT PRIMARY KEY,
    velocidad_mb INT NOT NULL,
    precio_mensual DECIMAL(10,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS cobertura (
    id_barrio INT AUTO_INCREMENT PRIMARY KEY,
    nombre_barrio VARCHAR(100) NOT NULL UNIQUE,
    estado_cobertura VARCHAR(10) NOT NULL DEFAULT 'OK'
);

CREATE TABLE IF NOT EXISTS clientes (
    dni VARCHAR(15) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    correo VARCHAR(100) UNIQUE,
    fecha_nacimiento DATE NOT NULL
);

-- 3. TABLA DEPENDIENTE (Relaciona todas las anteriores)
CREATE TABLE IF NOT EXISTS solicitudes (
    id_solicitud INT AUTO_INCREMENT PRIMARY KEY,
    dni_cliente VARCHAR(15) NOT NULL,
    id_barrio INT NOT NULL,
    id_servicio INT NOT NULL,
    calle VARCHAR(100) NOT NULL,
    numero INT NOT NULL,
    piso_dpto VARCHAR(20) DEFAULT NULL,
    tipo_solicitud VARCHAR(20) NOT NULL, 
    estado_instalacion VARCHAR(20) DEFAULT 'Pendiente', 
    fecha_visita DATE NOT NULL, 
    
    FOREIGN KEY (dni_cliente) REFERENCES clientes(dni) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (id_barrio) REFERENCES cobertura(id_barrio),
    FOREIGN KEY (id_servicio) REFERENCES servicios(id_servicio)
);

-- 4. CARGA DE DATOS INICIALES DE PRUEBA
INSERT INTO servicios (velocidad_mb, precio_mensual) VALUES 
(100, 12500.00), (300, 16800.00), (600, 23500.00), (1000, 31000.00);

/*
INSERT INTO cobertura (nombre_barrio, estado_cobertura) VALUES 
('Nueva Córdoba', 'OK'), ('Alta Córdoba', 'OK'), ('General Paz', 'OK'), 
('Centro', 'OK'), ('Cerro de las Rosas', 'OK'), ('San Vicente', 'NO OK'), 
('Villa El Libertador', 'NO OK'), ('Guiñazú', 'NO OK'),  ('Güemes', 'OK'), 
('Alberdi', 'NO OK');*/

-- 5. CARGA DE DATOS CLIENTES INICIALES DE PRUEBA
INSERT INTO clientes (
    dni,
    nombre,
    apellido,
    correo,
	fecha_nacimiento,
    numero_contacto
    )
VALUES (
	'45789231',
    'Sebastian',
    'Perez',
    'S.perez@gmail.com',
    '2005-05-02',
    '351676705'
);

ALTER TABLE clientes
ADD COLUMN numero_contacto VARCHAR(50) NOT NULL;