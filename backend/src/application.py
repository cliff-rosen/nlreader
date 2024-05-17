import os, time
import json
from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort
from flask_cors import CORS
from api import auth, hello
from datetime import datetime
from utils import gmail_api, utils, db


PORT = 5001

application = Flask(__name__)
CORS(application)

# logger.info('Initializing application...')


def get_session():
    auth_header = request.headers.get("Authorization")
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
            decoded_token = utils.decode_jwt(auth_token)
            print(decoded_token)
            if "error" in decoded_token:
                return {"user_id": -1}
        except IndexError:
            return {"user_id": -1}
    else:
        return {"user_id": -1}
    user = db.get_user_by_google_user_id(decoded_token["user_id_google"])
    # print("user", user)
    # decoded_token["access_token"] = user["access_token"]
    # decoded_token["refresh_token"] = user["refresh_token"]
    return user


class Login(Resource):
    def get(self):
        token = request.args.get("token")
        print("token:", token)
        user = auth.login(token)
        return user


class GetAuthUrl(Resource):
    def get(self):
        return {"url": gmail_api.get_auth_url()}


class GetTokenFromAuthCode(Resource):
    def get(self):
        session = get_session()
        print("session", session)
        auth_code = request.args.get("code")
        print("auth_code:", auth_code)
        auth.get_token_from_auth_code(session["user_id"], auth_code)
        return {"status": "SUCCESS"}


class Labels(Resource):
    def get(self):
        user = get_session()
        # print(user)
        creds_dict = json.loads(user["credentials"])
        creds = gmail_api.credentials_from_dict(creds_dict)
        service = gmail_api.get_service_from_creds(creds)
        print(service)
        labels = gmail_api.get_labels(service)
        # print("labels", labels)
        return labels


class Emails(Resource):
    def get(self):
        user = get_session()
        creds_dict = json.loads(user["credentials"])
        creds = gmail_api.credentials_from_dict(creds_dict)
        service = gmail_api.get_service_from_creds(creds)

        label = request.args.get("label")
        start_date = request.args.get("startDate")
        end_date = request.args.get("endDate")
        messages = gmail_api.get_messages(service, label, start_date, end_date)
        return messages


class Hello(Resource):
    def get(self):
        return hello.get_hello()

    def post(self):
        return hello.get_hello()


class Search(Resource):
    def get(self):
        start_date = request.args.get("startDate")
        end_date = request.args.get("endDate")
        poi = request.args.get("poi")
        doi = request.args.get("doi")
        min_score = request.args.get("minScore")
        max_score = request.args.get("maxScore")
        batch = 1

        articles = search.get_articles(
            batch, start_date, end_date, poi, doi, min_score, max_score
        )

        return {"result": "OK", "count": len(articles), "articles": articles[0:20]}


api = Api(application)

api.add_resource(Login, "/login")
api.add_resource(GetAuthUrl, "/get_auth_url")
api.add_resource(GetTokenFromAuthCode, "/get_token_from_auth_code")
api.add_resource(Labels, "/labels")
api.add_resource(Emails, "/emails")
api.add_resource(Hello, "/hello")
api.add_resource(Search, "/search")

if __name__ == "__main__":
    application.run(port=PORT, debug=True)
