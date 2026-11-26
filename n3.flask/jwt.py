from jose import jwt
from jose.exceptions import JWTError
from datetime import datetime, timedelta, timezone
from app import app

def generate_jwt(payload):
    dados = dict(payload)
    dados["exp"] = datetime.now(timezone.utc) + timedelta(hours=2)

    token = jwt.encode(
        dados,
        app.config["SECRET_KEY"],
        algorithm=app.config["ALGORITHM"]
    )

    return token


def verify_jwt(token):
    try:
        payload = jwt.decode(
            token,
            app.config["SECRET_KEY"],
            algorithms=[app.config["ALGORITHM"]]
        )

        return payload

    except JWTError as erro:
        print("Erro ao validar token:", erro)
        
