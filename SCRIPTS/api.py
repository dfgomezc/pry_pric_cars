#!/usr/bin/python

from flask import Flask
from flask_restx import Api, Resource, fields
import joblib
from model_deployment import predict_price
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins

api = Api(
    app, 
    version='1.0', 
    title='Predict car prices',
    description='Predecir el valor de un automovil a partir del anio, millage, el Estado en que se ubica, fabricante y linea')

ns = api.namespace('predict', 
     description='Prediccion de precios de automoviles')
   
parser = api.parser()

parser.add_argument(
    'Year', 
    type=str, 
    required=True, 
    help='Anio del vehiculo', 
    location='args',
    # action='append'
    )

parser.add_argument(
    'Mileage', 
    type=str, 
    required=True, 
    help='Millage del vehiculo', 
    location='args',
    # action='append'
    )

parser.add_argument(
    'State', 
    type=str, 
    required=True, 
    help='Estado en el que se vendio el vehiculo', 
    location='args',
    # action='append'
    )

parser.add_argument(
    'Make', 
    type=str, 
    required=True, 
    help='Fabricante del vehiculo', 
    location='args',
    # action='append'
    )

parser.add_argument(
    'Model', 
    type=str, 
    required=True, 
    help='linea del vehiculo', 
    location='args',
    # action='append'
    )


resource_fields = api.model('Resource', {
    'result': fields.String,
})


@ns.route('/')
class PriceCarApi(Resource):

    @api.doc(parser=parser)
    @api.marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()
        
        return {
         "result":  predict_price(args.Year,args.Mileage,args.State,args.Make, args.Model) 
        }, 200
    
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
