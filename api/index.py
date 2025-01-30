from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
users = [
    {"id": 1, "nombre": "Juan", "apellido": "Perez", "telefono": "987654321"},
    {"id": 2, "nombre": "Maria", "apellido": "Fernandez", "telefono": "9708654321"},
    {"id": 3, "nombre": "Pedro", "apellido": "Alvarez", "telefono": "987654321"},
    {"id": 4, "nombre": "Marcos", "apellido": "Silva", "telefono": "987123654"}
]
CORS(app)  

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "🦄🌈✨👋🌎🌍🌏✨🌈🦄"})

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "Usuario no encontrado"}), 404

@app.route('/api/users', methods=['POST'])
def add_user():
    user = request.get_json()
    if not user or not all(key in user for key in ["nombre", "apellido", "telefono"]):
        return jsonify({"error": "Datos de usuario incompletos"}), 400
    
    user['id'] = len(users) + 1
    users.append(user)
    return jsonify(user), 201
app.run()