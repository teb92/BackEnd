from flask import Flask, request, jsonify

app = Flask(__name__)

tareas = [
    {"id": 1, "titulo": "Comprar víveres", "descripcion": "Comprar leche, pan y huevos", "estado": "Por Hacer"},
    {"id": 2, "titulo": "Terminar informe", "descripcion": "Redactar el informe mensual para el equipo", "estado": "En Progreso"},
    {"id": 3, "titulo": "Hacer ejercicio", "descripcion": "Correr 5 km en el parque", "estado": "Completada"},
    {"id": 4, "titulo": "Leer un libro", "descripcion": "Leer 20 páginas del libro de ciencia ficción", "estado": "Por Hacer"}
]

FILE_PATH = "tareas.json"

# Funciones auxiliares para manejar el archivo JSON
def leer_tareas():
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Si el archivo no existe o está vacío, devuelve una lista vacía

def guardar_tareas(tareas):
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(tareas, file, indent=4, ensure_ascii=False)


@app.route("/")
def root():
    return "<h1>Hello, Lista!</h1>"

# Create, 

@app.route("/create", methods=["POST"])
def create_task():
    try:
        data = request.json
        if "id" not in request.json:
            raise ValueError("id missing from the body")
        
        if any(tarea["id"] == data["id"] for tarea in tareas):
            return jsonify(message="ID ya existente"), 400
        
        

        if "titulo" not in request.json:
            raise ValueError("titulo missing from the body")
        
        if "descripcion" not in request.json:
            raise ValueError("descripcion missing from the body")
        
        if "estado" not in request.json:
            raise ValueError("estado missing from the body")

        tareas.append(
            {
                "id": request.json["id"],
                "titulo": request.json["titulo"],
                "descripcion": request.json["descripcion"],
                "estado": request.json["estado"]
            }
        )
        return tareas
    except ValueError as ex:
        return jsonify(message=str(ex)), 400
    except Exception as ex:
        return jsonify(message=str(ex)), 500

# Read, 

@app.route("/read", methods=["GET"])
def read_task():
    filtered_task = tareas
    estado_filter = request.args.get("estado")
    if estado_filter:
        filtered_task = list(
            filter(lambda show: show["estado"] == estado_filter, filtered_task)
        )

    return {"data": filtered_task}




# Update, 

@app.route("/update/<int:id>", methods=["PATCH"])
def update_task(id):
    try:
        tarea = next((t for t in tareas if t["id"] == id), None)
        
        if tarea is None:
            return jsonify({"error": "Tarea no encontrada"}), 404
        data = request.json
        
        if "titulo" not in request.json:
            raise ValueError("titulo missing from the body")
        
        if "descripcion" not in request.json:
            raise ValueError("descripcion missing from the body")
        
        if "estado" not in request.json:
            raise ValueError("estado missing from the body")

        if "titulo" in data:
            tarea["titulo"] = data["titulo"]
        
        if "descripcion" in data:
            tarea["descripcion"] = data["descripcion"]
        
        if "estado" in data:
            tarea["estado"] = data["estado"]
            
        

        return jsonify({"mensaje": "Tarea actualizada", "tarea": tarea})
    
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500
# Delete

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_task(id):
    index = next((i for i, tarea in enumerate(tareas) if tarea["id"] == id), None)

    if index is None:
        return jsonify({"error": "Tarea no encontrada"}), 404

    eliminated_task = tareas.pop(index)  # Elimina la tarea de la lista
    return jsonify({"mensaje": "Tarea eliminada", "tarea": eliminated_task})

if __name__ == "__main__":
    app.run(host="localhost", port=5001, debug=True)