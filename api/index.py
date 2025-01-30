from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb+srv://Admin:Abc123.@cluster0.4ruo4.mongodb.net/")
db = client['express']
users_collection = db['usuarios']

#def user_to_json(user):
#    return {
#        "id": user.get("id", str(user["id"])),
#        "nombre": user["nombre"],
#        "apellido": user["apellido"],
#        "telefono": user["telefono"]
#    }
#@app.route('/api/users', methods=['GET'])
#def get_users():
#    users = list(users_collection.find())
#    return jsonify([user_to_json(user) for user in users])
#@app.route('/api/users/<string:user_id>', methods=['GET'])
#def get_user_by_id(user_id):
#    user = users_collection.find_one({"id": user_id}) 
#    if user:
#        return jsonify(user_to_json(user))
#    return jsonify({"error": "Usuario no encontrado"}), 404
#
#@app.route('/api/users', methods=['POST'])
#def add_user():
#    user = request.get_json()
#    if not user or not all(key in user for key in ["nombre", "apellido", "telefono"]):
#        return jsonify({"error": "Datos de usuario incompletos"}), 400
#    
#    result = users_collection.insert_one(user)
#    return jsonify({"id": str(result.inserted_id)}), 201

from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb+srv://Admin:Abc123.@cluster0.4ruo4.mongodb.net/")
db = client['express']
users_collection = db['usuarios']

# Convert ObjectId to string for JSON serialization
def user_to_json(user):
    return {
        "id": str(user["_id"]),  # Convert ObjectId to string
        "nombre": user["nombre"],
        "apellido": user["apellido"],
        "telefono": user["telefono"]
    }

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        users = list(users_collection.find())
        return jsonify([user_to_json(user) for user in users])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "API en Vercel funcionando correctamente"

# Export the app as "handler"
handler = app