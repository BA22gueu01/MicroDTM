from flask_restful import Resource, Api
from flask import Flask
import pandas as pd


class TrustscoreAPI(Resource):
    def get(self):
        data = pd.read_csv('trustscore.csv')
        data = data.to_dict()

        return {'data': data}, 200


class ParametersAPI(Resource):

    def get(self):
        data = pd.read_csv('parameters.csv')
        data = data.to_dict()

        return {'data': data}, 200


def flask():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(TrustscoreAPI, '/trustscore')
    #api.add_resource(ParametersAPI, '/parameters')
    app.run()


if __name__ == "__main__":
    flask()
