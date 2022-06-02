from flask_restful import Resource, Api
from flask import Flask, jsonify, make_response
import json


class TrustscoreAPI(Resource):
    def get(self):
        with open('trustscore.json', 'r') as f:
            data = json.loads(f.read())

        return make_response(jsonify(data), 200)


class ParametersAPI(Resource):
    def get(self):
        with open('parameterscore.json', 'r') as f:
            data = json.loads(f.read())

        return make_response(jsonify(data), 200)


class SubParametersAPI(Resource):
    def get(self):
        with open('subparameterscore.json', 'r') as f:
            data = json.loads(f.read())

        return make_response(jsonify(data), 200)


class SingleSubParametersAPI(Resource):
    def get(self):
        with open('singlesubparameterscore.json', 'r') as f:
            data = json.loads(f.read())

        return make_response(jsonify(data), 200)


def flask():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(TrustscoreAPI, '/trustscore')
    api.add_resource(ParametersAPI, '/parameters')
    api.add_resource(SubParametersAPI, '/subparameters')
    api.add_resource(SingleSubParametersAPI, '/singlesubparameters')
    app.run(host="0.0.0.0")


if __name__ == "__main__":
    flask()
