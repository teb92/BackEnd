 -- 1. CREAR TABLAS 

DROP TABLE IF EXISTS invoices;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE invoices (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    total NUMERIC(10, 2),
    status VARCHAR(50) DEFAULT 'completed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--  2. TRANSACCIÓN: COMPRA 

-- Ejemplo: el usuario con ID 1 compra 2 unidades del producto con ID 1

BEGIN;

DO $$
DECLARE
    product_stock INTEGER;
BEGIN
    SELECT stock INTO product_stock FROM products WHERE id = 1;
    IF product_stock < 2 THEN
        RAISE EXCEPTION 'Not enough stock available.';
    END IF;
END;
$$;

DO $$
DECLARE
    user_exists INTEGER;
BEGIN
    SELECT COUNT(*) INTO user_exists FROM users WHERE id = 1;
    IF user_exists = 0 THEN
        RAISE EXCEPTION 'User does not exist.';
    END IF;
END;
$$;

INSERT INTO invoices (user_id, product_id, quantity, total)
VALUES (1, 1, 2, (SELECT price FROM products WHERE id = 1) * 2);

UPDATE products
SET stock = stock - 2
WHERE id = 1;

COMMIT;

--  3. TRANSACCIÓN: RETORNO 

BEGIN;

DO $$
DECLARE
    invoice_exists INTEGER;
BEGIN
    SELECT COUNT(*) INTO invoice_exists
    FROM invoices
    WHERE id = 1 AND status = 'completed';

    IF invoice_exists = 0 THEN
        RAISE EXCEPTION 'Invoice does not exist or was already returned.';
    END IF;
END;
$$;

UPDATE products
SET stock = stock + (
    SELECT quantity FROM invoices WHERE id = 1
)
WHERE id = (
    SELECT product_id FROM invoices WHERE id = 1
);

UPDATE invoices
SET status = 'returned'
WHERE id = 1;

COMMIT;