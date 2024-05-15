from utils import utils, db, gmail_api


def login(token):
    user = utils.decode_google_jwt(token)
    print("login", user)
    res = db.get_user_by_google_user_id(user["sub"])
    if res["result"] == "SUCCESS":
        print("user found in DB")
        user = {
            "user_id": res["user_id"],
            "user_id_google": res["user_id_google"],
            "user_email": res["user_email"],
            "first_name": res["user_first_name"],
            "last_name": res["user_last_name"],
        }
        return {"user": user, "token": utils.make_jwt(user)}

    print("user not found in DB")
    user_id = db.insert_user(
        user["email"],
        user["sub"],
        user["given_name"],
        user["family_name"],
        "",
        "",
    )
    print("user_id:", user_id)
    user = {
        "user_id": user_id,
        "user_id_google": user["sub"],
        "user_email": user["email"],
        "first_name": user["given_name"],
        "last_name": user["family_name"],
        "token": utils.make_jwt(user),
    }
    return {"user": user}


def get_token_from_auth_code(auth_code):
    token = gmail_api.get_token_from_auth_code(auth_code)
    print("token", token)
    id_token = utils.decode_google_jwt(token["id_token"])
    user_id_google = id_token["sub"]
    access_token = token["access_token"]
    refresh_token = token["refresh_token"]
    db.update_user_authorization(user_id_google, access_token, refresh_token)
