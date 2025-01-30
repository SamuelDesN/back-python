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
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Setup logging
logging.basicConfig(level=logging.INFO)

# MongoDB connection URI (Ensure your password is URL encoded if it contains special characters)
client = MongoClient("mongodb+srv://Admin:Abc123.@cluster0.4ruo4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['express']
users_collection = db['usuarios']

# Helper function to convert user data to JSON format
def user_to_json(user):
    try:
        return {
            "id": str(user["_id"]),  # Convert ObjectId to string
            "nombre": user["nombre"],
            "apellido": user["apellido"],
            "telefono": user["telefono"]
        }
    except Exception as e:
        logging.error(f"Error converting user to JSON: {e}")
        return {"error": "Error converting user to JSON"}

# Route to get all users
@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        users = list(users_collection.find())
        if not users:
            logging.warning("No users found")
            return jsonify({"error": "No users found"}), 404
        return jsonify([user_to_json(user) for user in users])
    except Exception as e:
        logging.error(f"Error retrieving users: {str(e)}")
        return jsonify({"error": "Failed to retrieve users"}), 500

# Route to get a user by ID
@app.route('/api/users/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return jsonify(user_to_json(user))
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        logging.error(f"Error retrieving user by ID {user_id}: {str(e)}")
        return jsonify({"error": f"Error retrieving user with ID {user_id}"}), 500

# Route to add a new user
@app.route('/api/users', methods=['POST'])
def add_user():
    try:
        user = request.get_json()
        if not user or not all(key in user for key in ["nombre", "apellido", "telefono"]):
            return jsonify({"error": "Incomplete user data"}), 400

        result = users_collection.insert_one(user)
        return jsonify({"id": str(result.inserted_id)}), 201
    except Exception as e:
        logging.error(f"Error adding user: {str(e)}")
        return jsonify({"error": "Failed to add user"}), 500

# Home route
@app.route('/')
def home():
    return "API en Vercel funcionando correctamente"

# Handle Flask app execution
if __name__ == "__main__":
    app.run(debug=True)

# Expose the handler for Vercel
handler = app
