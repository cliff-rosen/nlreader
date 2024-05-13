import datetime
import local_secrets
from jwt import JWT

jwt_inst = JWT()


def make_jwt(user_id, username):
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
    }
    token = jwt.encode(payload, local_secrets.JWT_SECRET, algorithm="HS256")
    return token


def decode_jwt(jwt_token):
    try:
        decoded_token = jwt.decode(
            jwt_token, local_secrets.JWT_SECRET, algorithms=["HS256"]
        )
    except Exception as e:
        print("decode_token_error", e)
        return {"error", str(e)}
    return decoded_token


def decode_google_jwt(jwt):
    return jwt_inst.decode(jwt, do_verify=False)
