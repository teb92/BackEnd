CREATE TABLE Productos (
    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    precio INTEGER,
    fecha_ingreso TEXT,
    marca TEXT
);

CREATE TABLE Facturas (
    numero_factura INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_compra TEXT,
    correo_comprador TEXT,
    producto_id INTEGER,
    cantidad INTEGER,
    monto_total REAL,
    FOREIGN KEY (producto_id) REFERENCES Productos(codigo)
);

ALTER TABLE Facturas ADD telefonoComprador TEXT;

ALTER TABLE Facturas ADD codigoEmpleado INTEGER;

SELECT * FROM Productos;

SELECT * FROM Productos
WHERE precio > 50000;

SELECT * FROM Facturas
WHERE producto_id = 1;

SELECT producto_id, SUM(cantidad) AS total_comprado
FROM Facturas
GROUP BY producto_id;

SELECT * FROM Facturas
WHERE correo_comprador = 'ejemplo@ejemplo.com';

SELECT * FROM Facturas
ORDER BY monto_total DESC;

SELECT * FROM Facturas
WHERE numero_factura = 1;