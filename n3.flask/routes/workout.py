from flask import request, jsonify
from app import app, db
from model.workout import Workout
from jwt import verify_jwt

def get_logged_user():
    authorization = request.headers.get("Authorization", "")

    if not authorization.startswith("Bearer "):
        return None

    token = authorization.split(" ", 1)[1]
    return verify_jwt(token)


@app.route("/workouts", methods=["GET"])
def list_workouts():
    user = get_logged_user()

    if not user:
        return jsonify({"erro": "Acesso não autorizado."}), 401

    workouts = Workout.query.filter_by(user_id=user["id"]).all()

    return jsonify([
        {
            "id": item.id,
            "name": item.name,
            "description": item.description
        }
        for item in workouts
    ]), 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    user = get_logged_user()

    if not user:
        return jsonify({"erro": "Acesso não autorizado."}), 401

    data = request.get_json(silent=True) or {}

    name = data.get("name")
    description = data.get("description", "")

    if not name:
        return jsonify({"erro": "Informe o nome do treino."}), 400

    workout = Workout(
        name=name,
        description=description,
        user_id=user["id"]
    )

    db.session.add(workout)
    db.session.commit()

    return jsonify({
        "mensagem": "Treino cadastrado com sucesso!",
        "id": workout.id,
        "name": workout.name,
        "description": workout.description
    }), 201


@app.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    user = get_logged_user()

    if not user:
        return jsonify({"erro": "Acesso não autorizado."}), 401

    workout = Workout.query.filter_by(
        id=workout_id,
        user_id=user["id"]
    ).first()

    if not workout:
        return jsonify({"erro": "Treino não encontrado."}), 404

    db.session.delete(workout)
    db.session.commit()

    return jsonify({
        "mensagem": "Treino excluído com sucesso."
    }), 200