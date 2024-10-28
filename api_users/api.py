from flask import Flask, jsonify, request, make_response, abort

from database import db
from models.users import USERS, USERSEncoder

app = Flask(__name__)
app.config['DEBUG'] = True
app.json_encoder = USERSEncoder


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Status': 404, 'Error': 'Resource not found'}), 404)


@app.route("/api/v1/resources/home", methods=['GET'])
def home():
    return "<h1>andre dias</h1>"


@app.route("/api/v1/resources/users", methods=['GET'])
def lists():
    usuarios_serializaveis = [usuario.__dict__ for usuario in db]
    return jsonify({'Usuários': usuarios_serializaveis})


@app.route("/api/v1/resources/users/<int:user_id>", methods=['GET'])
def get_user(user_id):
    user = next((usuario for usuario in db if usuario.id == user_id), None)
    if user is not None:
        return jsonify(user.__dict__)
    else:
        return jsonify({'Status': 404, 'Error': 'User not found'}), 404
    

@app.route("/api/v1/resources/users", methods=['GET', 'POST'])
def manage_user():
    if request.method == 'POST':
        
        data = request.get_json()
        
        
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
       
        new_user = USERS(name, email, password)
        
        
        db.append(new_user)
        
       
        return jsonify(new_user.__dict__), 201

    usuarios_serializaveis = [usuario.__dict__ for usuario in db]
    return jsonify({'Usuários': usuarios_serializaveis})


@app.route("/api/v1/resources/users/<int:user_id>", methods=['GET', 'POST', 'PUT'])
def add_user(user_id):

    if request.method == 'PUT':
        user = next((usuario for usuario in db if usuario.id == user_id), None)
        
        if user is not None:
            data = request.get_json()
            user.name = data.get('name', user.name)  
            user.email = data.get('email', user.email)  
            user.password = data.get('password', user.password) 
            
            return jsonify(user.__dict__), 200
        else:
            return jsonify({'Status': 404, 'Error': 'User not found'}), 404
        
@app.route("/api/v1/resources/users/<int:user_id>", methods=['DELETE'])
def delete_user(user_id):

    if request.method == 'DELETE':
        user = next((usuario for usuario in db if usuario.id == user_id), None)
        
        if user is not None:
            db.remove(user)  
            return jsonify({'Status': 200, 'Message': 'Usuario excluido com sucesso.'}), 200
        else:
            return jsonify({'Status': 404, 'Error': 'User not found'}), 404      


app.run()