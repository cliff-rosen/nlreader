from utils import utils, db


def login(token):
    user = utils.decode_google_jwt(token)
    print("login", user)
    res = db.get_user_by_google_user_id(user["sub"])
    if res["result"] == "SUCCESS":
        print("user found in DB")
        return {
            "user_id": res["user_id"],
            "user_id_google": res["user_id_google"],
            "user_email": res["user_email"],
            "first_name": res["user_first_name"],
            "last_name": res["user_last_name"],
            "access_token": res["access_token"],
            "refresh_token": res["refresh_token"],
        }

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
    return {
        "user_id": user_id,
        "user_id_google": user["sub"],
        "user_email": user["email"],
        "first_name": user["given_name"],
        "last_name": user["family_name"],
        "access_token": "",
        "refresh_token": "",
    }
