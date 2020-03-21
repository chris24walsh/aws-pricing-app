from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
import requests
import json
import re
from collections import OrderedDict
import boto3

app = Flask(__name__)
api = Api(app)
session = requests.Session()

class Service_price(Resource):
    def get(self, service_code, filter_type, filter_field, filter_value):
        # start boto3 session
        session = boto3.Session()
        # make aws pricing get-product call, using arguments as parameters
        p = session.client('pricing', region_name='us-east-1') 
        response = p.get_products(
            ServiceCode=service_code,
            Filters=[
                {
                    'Type': filter_type,
                    'Field': filter_field,
                    'Value': filter_value
                },
            ]#,
            #FormatVersion='string',
            #NextToken='string',
            #MaxResults=123
        )
        # return json string, in some kinda digest
        return json.dumps(response['PriceList'])


# Api routes
api.add_resource(Service_price, '/service_price/service_code=<string:service_code>&filter_type=<string:filter_type>&filter_field=<string:filter_field>&filter_value=<string:filter_value>')

# Functions:


if __name__ == '__main__':
   app.run(debug='True',host='0.0.0.0',port='5002')
