import datetime
import local_secrets
import jwt
from authlib.jose import JsonWebEncryption


def make_jwt_for_user(user_id, username):
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
    }
    token = jwt.encode(payload, local_secrets.JWT_SECRET, algorithm="HS256")
    return token


def make_jwt(payload):
    return jwt.encode(payload, local_secrets.JWT_SECRET)


def decode_jwt(jwt_token):
    try:
        decoded_token = jwt.decode(
            jwt_token, local_secrets.JWT_SECRET, algorithms="HS256"
        )

    except Exception as e:
        print("decode_token_error", e)
        return {"error", str(e)}
    return decoded_token


def decode_google_jwt(token):
    return jwt.decode(token, options={"verify_signature": False})
