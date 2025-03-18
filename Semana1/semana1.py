from flask import Flask, request, jsonify
import json
app = Flask(__name__)


FILE_PATH = "tareas.json"
def read_tasks_from_file():
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError): 
        return []  

def write_task(tareas):
    try:
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(tareas, file, indent=4, ensure_ascii=False)
    except Exception as ex:
        print(f"Error al escribir en el archivo: {ex}")


@app.route("/")
def root():
    return "<h1>Hello, Lista!</h1>"

# Create

@app.route("/create", methods=["POST"])
def create_task():
    try:
        data = request.json
        
        if not isinstance(data, dict):
            return jsonify({"error": "Invalid JSON format"}), 400

        required_fields = ["id", "titulo", "descripcion", "estado"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos obligatorios"}), 400

        tareas = read_tasks_from_file()
        if any(t["id"] == data["id"] for t in tareas):
            return jsonify({"error": "El ID ya existe."}), 400

        tareas.append(data)
        write_task(tareas)

        return jsonify({"mensaje": "Tarea creada", "tarea": data}), 201

    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

# Read

@app.route("/read", methods=["GET"])
def read_task():
    tareas = read_tasks_from_file()
    estado_filter = request.args.get("estado") 
    
    if estado_filter:
        tareas = [t for t in tareas if t["estado"] == estado_filter]

    return jsonify({"data": tareas})

# Update 

@app.route("/update/<int:id>", methods=["PATCH"])
def update_task(id):
    try:
        tareas = read_tasks_from_file()
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
            
        

        write_task(tareas)
        return jsonify({"mensaje": "Tarea actualizada", "tarea": tarea})
    
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500
# Delete

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_task(id):
    try:
        tareas = read_tasks_from_file()
        index = next((i for i, tarea in enumerate(tareas) if tarea["id"] == id), None)

        if index is None:
            return jsonify({"error": "Tarea no encontrada"}), 404

        eliminated_task = tareas.pop(index)  
        write_task(tareas)

        return jsonify({"mensaje": "Tarea eliminada", "tarea": eliminated_task})

    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

if __name__ == "__main__":
    app.run(host="localhost", port=5001, debug=True)