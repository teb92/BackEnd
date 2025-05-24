-- 1. Un script que agregue un usuario nuevo
INSERT INTO lyfter_car_rental.users (first_name, last_name, email, password, date_of_birth, account_state)
VALUES ('Laura', 'Smith', 'laura.smith@example.com', 'StrongPassword123!', '1990-06-15', true);

-- 2. Un script que agregue un automovil nuevo
INSERT INTO lyfter_car_rental.cars (brand, model, year, state)
VALUES ('Toyota', 'Corolla', '2020', 'available');

-- 3. Un script que cambie el estado de un usuario
UPDATE lyfter_car_rental.users
SET account_state = false
WHERE email = 'laura.smith@example.com';

-- 4. Un script que cambie el estado de un automovil
UPDATE lyfter_car_rental.cars
SET state = 'rented'
WHERE id = 5;

-- 5. Un script que genere un alquiler nuevo con los datos de un usuario y un automovil
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_date, rental_status)
VALUES (1, 5, NOW(), 'active');

-- 6. Un script que confirme la devolución del auto al completar el alquiler, 
-- colocando el auto como disponible y completando el estado del alquiler
UPDATE lyfter_car_rental.rentals
SET rental_status = 'completed'
WHERE user_id = 1 AND car_id = 5 AND rental_status = 'active';

UPDATE lyfter_car_rental.cars
SET state = 'available'
WHERE id = 5;

-- 7. Un script que deshabilite un automovil del alquiler
UPDATE lyfter_car_rental.cars
SET state = 'disabled'
WHERE id = 10;

-- 8. Un script que obtenga todos los automoviles alquilados, y otro que obtenga todos los disponibles.
-- Autos alquilados
SELECT * FROM lyfter_car_rental.cars
WHERE state = 'rented';

-- Autos disponibles
SELECT * FROM lyfter_car_rental.cars
WHERE state = 'available';