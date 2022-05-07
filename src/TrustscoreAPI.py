from flask_restful import Resource
import pandas as pd


class TrustscoreAPI(Resource):

    def get(self):
        data = pd.read_csv('trustscore.csv')
        data = data.to_dict()

        return {'data': data}, 200
