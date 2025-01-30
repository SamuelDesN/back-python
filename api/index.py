from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient, errors
from bson import ObjectId
import logging

app = Flask(__name__)
CORS(app)

# Add logging
logging.basicConfig(level=logging.INFO)

client = MongoClient("mongodb+srv://Admin:Abc123.@cluster0.4ruo4.mongodb.net/", serverSelectionTimeoutMS=5000)
db = client['express']
users_collection = db['usuarios']

@app.route('/')
def home():
    return "API en Vercel funcionando correctamente"

def user_to_json(user):
    return {
        "id": str(user["_id"]),
        "nombre": user["nombre"],
        "apellido": user["apellido"],
        "telefono": user["telefono"]
    }

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        users = list(users_collection.find())
        return jsonify([user_to_json(user) for user in users])
    except errors.PyMongoError as e:
        logging.error(f"Error fetching users: {e}")
        return jsonify({"error": "Database error"}), 500

@app.route('/api/users/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        user = users_collection.find_one({"id": user_id})
        if user:
            return jsonify(user_to_json(user))
        return jsonify({"error": "Usuario no encontrado"}), 404
    except errors.PyMongoError as e:
        logging.error(f"Error fetching user by ID: {e}")
        return jsonify({"error": "Database error"}), 500

@app.route('/api/users', methods=['POST'])
def add_user():
    try:
        user = request.get_json()
        if not user or not all(key in user for key in ["nombre", "apellido", "telefono"]):
            return jsonify({"error": "Datos de usuario incompletos"}), 400
        
        result = users_collection.insert_one(user)
        return jsonify({"id": str(result.inserted_id)}), 201
    except errors.PyMongoError as e:
        logging.error(f"Error inserting user: {e}")
        return jsonify({"error": "Database error"}), 500

app.run(debug=True)
handler = app
