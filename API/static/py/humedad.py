import os, pandas as pd
from flask import request
from flask_restful import Resource

# Clase para manejar el recurso
class Endpoint_Sensor_Humedad(Resource):

    def get(self):
        '''
        '''
        location_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        file_path = os.path.join(
            location_path,
            "static",
            'data',
            'sensor_humedad.csv'
        )
        file_data = pd.read_csv(file_path,index_col = 'ID')
        file_data = file_data.to_dict()

        return file_data,200
    
    def post(self):
        '''
        '''

        # ===== Validacion de datos
        data = request.json
        if not("valor" in data):
            return {"error": "Falta el campo 'valor'"}, 400
        
        # ===== Obtencion de valores
        valor = data['valor']
        
        # ===== Pipeline
        location_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        file_path = os.path.join(
            location_path,
            "static",
            'data',
            'sensor_humedad.csv'
        )
        file_data = pd.read_csv(file_path,)
        file_data.loc[len(file_data)] = [len(file_data)+1, valor]
        file_data.to_csv(file_path,index=False)

        # ===== Confirmacion
        return {"estatus": "Mensaje agregado", "valor": valor }, 201
