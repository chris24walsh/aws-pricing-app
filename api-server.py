from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
import requests
import json, yaml, json2html
import re
from collections import OrderedDict
import boto3

app = Flask(__name__)
api = Api(app)
requests_session = requests.Session()
boto3_session = boto3.Session()
p = boto3_session.client('pricing', region_name='us-east-1') 

class describe_services(Resource):
    def get(self, service_code="All"):
        if service_code == "All":
            response = p.describe_services()
            print('Service code is empty')
        else:
            response = p.describe_services(
                ServiceCode=service_code#,
                #FormatVersion='string',
                #NextToken='string',
                #MaxResults=123
            )
        # return json string, in some kinda digest
        return response['Services']#[0]['AttributeNames']

class get_products(Resource):
    def get(self, service_code, filter_type, filter_field, filter_value):
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
        
        return response['PriceList']#[0]


# Api routes
api.add_resource(describe_services, '/describe_services/service_code=<string:service_code>')
api.add_resource(get_products, '/get_products/service_code=<string:service_code>&filter_type=<string:filter_type>&filter_field=<string:filter_field>&filter_value=<string:filter_value>')

# Functions:


if __name__ == '__main__':
   app.run(debug='True',host='0.0.0.0',port='5002')
