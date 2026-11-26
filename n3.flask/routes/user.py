from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from model.user import User
from jwt import generate_jwt

@app.route("/users", methods=["GET"])
def list_users():
    users = User.query.order_by(User.id.asc()).all()
    return jsonify([
        {"id": user.id, "username": user.username, "email": user.email}
        for user in users
    ]), 200

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"erro": "Preencha nome, email e senha."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"erro": "Este email já está cadastrado."}), 409

    user = User(
        username=username,
        email=email,
        password=generate_password_hash(password)
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "mensagem": "Aluno cadastrado com sucesso!",
        "id": user.id,
        "username": user.username,
        "email": user.email
    }), 201

@app.route("/login", methods=["POST"])
def login_user():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"erro": "Informe email e senha."}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"erro": "Email ou senha incorretos."}), 401

    token = generate_jwt({"id": user.id, "email": user.email})
    return jsonify({
        "mensagem": "Login realizado com sucesso!",
        "token": token
    }), 200
