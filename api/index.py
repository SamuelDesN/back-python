from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

handler = app
CORS(app)

try:
    client = MongoClient("mongodb+srv://Admin:Abc123.@cluster0.4ruo4.mongodb.net/")
    db = client['express']
    users_collection = db['usuarios']
    # Optional: Check if the connection is successful
    client.admin.command('ping')
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise e  # Re-raise the exception to stop execution

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

handler = app
