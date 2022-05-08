from flask_restful import Resource, Api
from flask import Flask, jsonify, make_response
import pandas as pd
import json


class TrustscoreAPI(Resource):
    def get(self):
        #data = pd.read_csv('trustscore.csv', delimiter=',')
        #data = data.to_json()
        with open('trustscore.json', 'r') as f:
            data = json.loads(f.read())

        #data = pd.read_json('trustscore.json')

        #return {"data": data}, 200
        return make_response(jsonify(data), 200)


class ParametersAPI(Resource):

    def get(self):
        data = pd.read_csv('parameters.csv')
        data = data.to_json()

        return {"data": data}, 200


def flask():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(TrustscoreAPI, '/trustscore')
    #api.add_resource(ParametersAPI, '/parameters')
    app.run(host="0.0.0.0")


if __name__ == "__main__":
    flask()
