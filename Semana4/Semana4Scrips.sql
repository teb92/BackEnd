-- Tabla de Libros
CREATE TABLE Books (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Author INTEGER,
    FOREIGN KEY (Author) REFERENCES Authors(ID)
);

-- Tabla de Autores
CREATE TABLE Authors (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL
);

-- Tabla de Clientes
CREATE TABLE Customers (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Email TEXT NOT NULL
);

-- Tabla de Rentas
CREATE TABLE Rents (
    ID INTEGER PRIMARY KEY,
    BookID INTEGER NOT NULL,
    CustomerID INTEGER NOT NULL,
    State TEXT NOT NULL,
    FOREIGN KEY (BookID) REFERENCES Books(ID),
    FOREIGN KEY (CustomerID) REFERENCES Customers(ID)
);

SELECT b.Name AS Book, a.Name AS Author
FROM Books b
LEFT JOIN Authors a ON b.AuthorID = a.ID;

SELECT b.Name
FROM Books b
LEFT JOIN Authors a ON b.AuthorID = a.ID
WHERE a.ID IS NULL;

SELECT a.Name
FROM Authors a
LEFT JOIN Books b ON b.AuthorID = a.ID
WHERE b.ID IS NULL;

SELECT DISTINCT b.Name
FROM Books b
JOIN Rents r ON b.ID = r.BookID;

SELECT b.Name
FROM Books b
LEFT JOIN Rents r ON b.ID = r.BookID
WHERE r.ID IS NULL;

SELECT c.Name
FROM Customers c
LEFT JOIN Rents r ON c.ID = r.CustomerID
WHERE r.ID IS NULL;

SELECT DISTINCT b.Name
FROM Books b
JOIN Rents r ON b.ID = r.BookID
WHERE r.Status = 'Overdue';

