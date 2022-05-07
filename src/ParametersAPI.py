from flask_restful import Resource
import pandas as pd


class ParametersAPI(Resource):

    def get(self):
        data = pd.read_csv('parameters.csv')
        data = data.to_dict()

        return {'data': data}, 200
