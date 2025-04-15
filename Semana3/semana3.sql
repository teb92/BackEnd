--1. Cree una nueva base de datos en SQLite.
--2. Replique las tablas creadas anteriormente en [Ejercicios de Bases de Datos](https://www.notion.so/Ejercicios-de-Bases-de-Datos-658771fec5744ac8af4467f44446f57b?pvs=21), con sus respectivos PKs, FKs, constraints, y demás requerimientos.
--    1. Investigue cómo hacer que los `PKs` se generen **automáticamente**.
--    2. Utilice los tipos de datos adecuados. 
--    3. Si existe alguna limitante por SQLite, documéntela y resuelva la limitante como considere adecuado.

-- Limitaciones de SQLite
--	No tiene tipo DATE o DATETIME: se usan TEXT en formato ISO 8601 (YYYY-MM-DD).
--	No soporta CHECK constraints complejos ni tipos estrictos.

CREATE TABLE Products (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Price REAL NOT NULL,
    EntryDate TEXT NOT NULL, -- formato ISO: YYYY-MM-DD
    Brand TEXT
);

CREATE TABLE Bills (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    PurchaseDate TEXT NOT NULL, -- formato ISO: YYYY-MM-DD
    Email TEXT NOT NULL,
    Total REAL NOT NULL
);

CREATE TABLE BillProducts (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    BillsID INTEGER NOT NULL,
    ProductsID INTEGER NOT NULL,
    Amount INTEGER NOT NULL,
    Total REAL NOT NULL,
    FOREIGN KEY (BillsID) REFERENCES Bills(ID),
    FOREIGN KEY (ProductsID) REFERENCES Products(ID)
);

CREATE TABLE ShoppingCart (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Total REAL NOT NULL
);

CREATE TABLE ShoppingCartDetail (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    ShoppingCartID INTEGER NOT NULL,
    ProductsID INTEGER NOT NULL,
    Amount INTEGER NOT NULL,
    Total REAL NOT NULL,
    FOREIGN KEY (ShoppingCartID) REFERENCES ShoppingCart(ID),
    FOREIGN KEY (ProductsID) REFERENCES Products(ID)
);

--Modifique la tabla de Facturas creada en el ejercicio anterior y 
--agregue una columna para almacenar también el número de teléfono del comprador, 
--y otra para el código de empleado del cajero que realizó la venta.

ALTER TABLE Bills
ADD COLUMN PhoneNumber TEXT;

ALTER TABLE Bills
ADD COLUMN EmployeeID INTEGER;

--4. Realice los siguientes `SELECT`:
--    1. Obtenga todos los productos almacenados

SELECT * 
FROM Products;

--    2. Obtenga todos los productos que tengan un precio mayor a 50000

SELECT * 
FROM Products 
WHERE Price > 50000;

--    3. Obtenga todas las compras de un mismo producto por id.
-- actualizado
SELECT 
    b.ID AS purchases, --Obtenga todas las compras
    p.ProductsID
FROM BillProducts p
JOIN Bills b ON p.BillsID = b.ID
WHERE p.ProductsID = 1;

--    4. Obtenga todas las compras agrupadas por producto,
-- donde se muestre el total comprado entre todas las compras.

SELECT ProductsID, SUM(Amount) AS TotalPurchased
FROM BillProducts
GROUP BY ProductsID;

--    5. Obtenga todas las facturas realizadas por el mismo comprador

SELECT Email, COUNT(*) AS FacturasTotales
FROM Bills
GROUP BY Email;

--or

SELECT *
FROM Bills
WHERE Email = 'XXXX';

--    6. Obtenga todas las facturas ordenadas por monto total de forma descendente

SELECT *
FROM Bills
ORDER BY Total DESC;

--    7. Obtenga una sola factura por número de factura.

SELECT *
FROM Bills
WHERE ID = 1;