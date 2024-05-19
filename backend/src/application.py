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
        print("reading credentials from dictionary")
        creds = gmail_api.credentials_from_dict(json.loads(user["credentials"]))
        print("building service")
        service = gmail_api.get_service_from_creds(creds)
        print("retrieving labels")
        labels = gmail_api.get_labels(service)
        print("labels", labels)
        return labels


class Messages(Resource):
    def get(self):
        user = get_session()
        creds_dict = json.loads(user["credentials"])
        creds = gmail_api.credentials_from_dict(creds_dict)
        service = gmail_api.get_service_from_creds(creds)

        label = request.args.get("label")
        start_date = request.args.get("startDate")
        end_date = request.args.get("endDate")
        messages = gmail_api.get_messages(service, label, start_date, end_date)
        batch_id = db.insert_batch(label, "-", start_date, end_date)
        # for message in messages:
        #     db.insert_message(
        #         batch_id,
        #         message["message_date"],
        #         message["message_sender"],
        #         message["message_subject"],
        #         message["message_body"],
        #         message["message_body_html"],
        #     )
        print(messages[:1])
        return {"messages": messages, "batch_id": batch_id}


class Batches(Resource):
    def get(self):
        user = get_session()
        batch_id = request.args.get("batch_id")
        messages = db.get_messages_by_batch_id(batch_id)
        return {"messages": messages, "batch_id": batch_id}


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
api.add_resource(Messages, "/messages")
api.add_resource(Batches, "/batches")
api.add_resource(Hello, "/hello")
api.add_resource(Search, "/search")

if __name__ == "__main__":
    application.run(port=PORT, debug=True)
