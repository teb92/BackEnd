from flask import Flask, request, jsonify
from psycopg2 import sql
from db import get_connection

app = Flask(__name__)

def set_search_path(cursor):
    cursor.execute("SET search_path TO lyfter_car_rental")

# ------------------ Creación ------------------
# Crear un usuario nuevo
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        set_search_path(cursor)
        cursor.execute("""
            INSERT INTO users  (first_name, last_name, email, password, date_of_birth, account_state)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (
            data['first_name'],
            data['last_name'],
            data['email'],
            data['password'],
            data['date_of_birth'],
            True
        ))
        user_id = cursor.fetchone()[0]
        conn.commit()
        return jsonify({"id": user_id, **data}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
# Crear un automovil nuevo
@app.route('/cars', methods=['POST'])
def create_car():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        set_search_path(cursor)
        cursor.execute("""
            INSERT INTO automoviles (car_brand, model, year, state)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """, (
            data['car_brand'],
            data['model'],
            data['year'],
            data['state']
        ))
        car_id = cursor.fetchone()[0]
        conn.commit()
        return jsonify({"id": car_id, **data}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
# Crear un alquiler nuevo
@app.route('/rentals', methods=['POST'])
def create_rental():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        set_search_path(cursor)
        cursor.execute("""
            INSERT INTO rentals (user_id, car_id, rental_status)
            VALUES (%s, %s, %s)
            RETURNING id;
        """, (
            data['user_id'],
            data['car_id'],
            'ongoing'
        ))
        rental_id = cursor.fetchone()[0]
        conn.commit()
        return jsonify({"id": rental_id, **data}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ------------------ Modificación ------------------
# Cambiar el estado de un automovil
@app.route('/cars/<int:car_id>/status', methods=['PUT'])
def update_car_status(car_id):
    data = request.json  # expects 'state': 'available' or 'unavailable'
    try:
        conn = get_connection()
        cursor = conn.cursor()
        set_search_path(cursor)
        cursor.execute("""
            UPDATE automoviles SET state = %s WHERE id = %s;
        """, (data['state'], car_id))
        conn.commit()
        return jsonify({"id": car_id, **data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
# Cambiar el estado de un usuario
@app.route('/users/<int:user_id>/status', methods=['PUT'])
def update_user_status(user_id):
    data = request.json  
    try:
        conn = get_connection()
        cursor = conn.cursor()
        set_search_path(cursor)
        cursor.execute("""
            UPDATE users  SET account_state = %s WHERE id = %s;
        """, (data['account_state'], user_id))
        conn.commit()
        return jsonify({"id": user_id, **data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
# Completar un alquiler
@app.route('/rentals/<int:rental_id>/complete', methods=['PUT'])
def complete_rental(rental_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        set_search_path(cursor)
        cursor.execute("""
            UPDATE rentals SET rental_status = 'completed' WHERE id = %s;
        """, (rental_id,))
        conn.commit()
        return jsonify({"id": rental_id, "status": "completed"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
#Cambiar el estado de un alquiler
@app.route('/rentals/<int:rental_id>/status', methods=['PUT'])
def update_rental_status(rental_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        set_search_path(cursor)
        cursor.execute("""
            UPDATE rentals SET rental_status = %s WHERE id = %s;
        """, (data['status'], rental_id))
        conn.commit()
        return jsonify({"id": rental_id, "status": data['status']}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
#Flagear un usuario como moroso
@app.route('/users/<int:user_id>/debtor', methods=['PUT'])
def flag_user_as_debtor(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        set_search_path(cursor)
        cursor.execute("""
            UPDATE users SET account_state = FALSE WHERE id = %s;
        """, (user_id,))
        conn.commit()
        return jsonify({"id": user_id, "account_state": False}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ------------------ Listado ------------------
#Listar todos los usuarios
@app.route('/users', methods=['GET'])
def list_users():
    filters = request.args
    try:
        conn = get_connection()
        cursor = conn.cursor()
        set_search_path(cursor)

        base_query = sql.SQL("SELECT * FROM users")
        conditions = []
        values = []

        for key, value in filters.items():
            conditions.append(sql.SQL("{} ILIKE %s").format(sql.Identifier(key)))
            values.append(f"%{value}%")

        if conditions:
            base_query += sql.SQL(" WHERE ") + sql.SQL(" AND ").join(conditions)

        cursor.execute(base_query, values)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        users = [dict(zip(columns, row)) for row in rows]
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
        
#Listar todos los automoviles
@app.route('/vehicles', methods=['GET'])
def list_vehicles():
    filters = request.args
    try:
        conn = get_connection()
        cursor = conn.cursor()
        set_search_path(cursor)

        base_query = sql.SQL("SELECT * FROM vehicles")
        conditions = []
        values = []

        for key, value in filters.items():
            conditions.append(sql.SQL("{} ILIKE %s").format(sql.Identifier(key)))
            values.append(f"%{value}%")

        if conditions:
            base_query += sql.SQL(" WHERE ") + sql.SQL(" AND ").join(conditions)

        cursor.execute(base_query, values)
        vehicles = cursor.fetchall()
        return jsonify(vehicles), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
        
#Listar todos los alquileres
        
@app.route('/rentals', methods=['GET'])
def list_rentals():
    filters = request.args
    try:
        conn = get_connection()
        cursor = conn.cursor()
        set_search_path(cursor)

        base_query = sql.SQL("SELECT * FROM rentals")
        conditions = []
        values = []

        for key, value in filters.items():
            conditions.append(sql.SQL("{} ILIKE %s").format(sql.Identifier(key)))
            values.append(f"%{value}%")

        if conditions:
            base_query += sql.SQL(" WHERE ") + sql.SQL(" AND ").join(conditions)

        cursor.execute(base_query, values)
        rentals = cursor.fetchall()
        return jsonify(rentals), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
# ------------------ Ejecutar ------------------

if __name__ == '__main__':
    app.run(debug=True)