from flask import Flask, request, jsonify
from models.user import User
from models.meal import Meal
from database import db
from datetime import datetime, timezone
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = "admin"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:admin123@127.0.0.1:3306/flask-crud"

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
            login_user(user)
            return jsonify({"message": "Autenticação realizada"})
        
    return jsonify({"message": "Credenciais inválidas"}), 404

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return jsonify({"message": "Usuário deslogado com sucesso"})

@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso"})

    return jsonify({"message": "Preencha corretamente os dados"}), 400

# Register a meal
@app.route("/meal", methods=['POST'])
@login_required
def register_meal():
    data = request.json
    user_id = current_user.id
    name = data.get('name')
    description = data.get('description')
    is_in_diet = data.get('is_in_diet')

    if name and description:
        new_meal = Meal(user_id=user_id, name=name, description=description, is_in_diet=is_in_diet)
        db.session.add(new_meal)
        db.session.commit()
        return jsonify({"message": "Refeição cadastrada com sucesso"})
    
    return jsonify({"message": "Preencha corretamente os dados"}), 400

# Edit a meal
@app.route("/meal/<int:meal_id>", methods=['PUT'])
@login_required
def edit_meal(meal_id):
    data = request.json
    current_meal = Meal.query.get(meal_id)

    if current_meal.user_id != current_user.id:
        return jsonify({"message": "Você não possui permissão para editar essa refeição"}), 403

    if current_meal:
        current_meal.name = data.get("name")
        current_meal.description = data.get("description")
        current_meal.is_in_diet = data.get("is_in_diet")
        db.session.commit()
        return jsonify({"message": f"Refeição atualizada com sucesso"})
    
    return jsonify({"message": "Refeição não encontrada"}), 404

# Delete a meal
@app.route("/meal/<int:meal_id>", methods=['DELETE'])
@login_required
def delete_meal(meal_id):
    meal = Meal.query.get(meal_id)

    if meal.user_id!= current_user.id:
        return jsonify({"message": "Você não possui permissão para excluir essa refeição"}), 403
    
    if meal:
        db.session.delete(meal)
        db.session.commit()
        return jsonify({"message": "Refeição excluída com sucesso"})

    return jsonify({"message": "Refeição não encontrada"}), 404

# List all user meals

# List a specific meal

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)
