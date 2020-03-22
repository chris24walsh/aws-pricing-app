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

class api_help(Resource):
    def get(self, command=""):
        help_h = "/, /help, /help/<command>"
        help_ds = "/describe_services/service_code=<string:service_code>"
        help_gav = "/get_attribute_values/service_code=<string:service_code>&attribute_name=<string:attribute_name>"
        help_gp = "/get_products/service_code=<string:service_code>&filter_type=<string:filter_type>&filter_field=<string:filter_field>&filter_value=<string:filter_value>"
        help_all = ["The following api routes are available:", help_h, help_ds, help_gav, help_gp]
        help_info = str()
        if command == "describe_services":
            help_info = help_ds
        elif command == "get_attribute_values":
            help_info = help_gav
        elif command == "get_products":
            help_info = help_gp
        else:
            help_info = help_all
        return help_info

class describe_services(Resource):
    def get(self, service_code="All"):
        if service_code == "All":
            response = p.describe_services()
        else:
            response = p.describe_services(
                ServiceCode=service_code#,
                #FormatVersion='string',
                #NextToken='string',
                #MaxResults=123
            )
        return response['Services']

class get_attribute_values(Resource):
    def get(self, service_code, attribute_name):
        response = p.get_attribute_values(
            ServiceCode=service_code,
            AttributeName=attribute_name#,
            #NextToken='string',
            #MaxResults=123
        ) 
        return response['AttributeValues']

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
        
        return response['PriceList']


# Api routes
api.add_resource(api_help, '/', '/help', '/help/<command>')
api.add_resource(describe_services, '/describe_services/service_code=<string:service_code>')
api.add_resource(get_attribute_values, '/get_attribute_values/service_code=<string:service_code>&attribute_name=<string:attribute_name>')
api.add_resource(get_products, '/get_products/service_code=<string:service_code>&filter_type=<string:filter_type>&filter_field=<string:filter_field>&filter_value=<string:filter_value>')

# Functions:


if __name__ == '__main__':
   app.run(debug='True',host='0.0.0.0',port='5002')
