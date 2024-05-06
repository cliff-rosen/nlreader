import time
from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort
from flask_cors import CORS
from api import search, hello
from datetime import datetime
from utils import gmail_api

PORT = 5001

application = Flask(__name__)
CORS(application)

# logger.info('Initializing application...')

parser = reqparse.RequestParser()
parser.add_argument("domain_id", type=int)


class GetAuthUrl(Resource):
    def get(self):
        return {"url": gmail_api.get_auth_url()}


class GetTokenFromAuthCode(Resource):
    def get(self):
        return "done"


class Hello(Resource):
    def get(self):
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
api.add_resource(Hello, "/hello")
api.add_resource(GetAuthUrl, "/get_auth_url")
api.add_resource(GetTokenFromAuthCode, "/get_token_from_auth_code")
api.add_resource(Search, "/search")

if __name__ == "__main__":
    application.run(port=PORT, debug=True)
