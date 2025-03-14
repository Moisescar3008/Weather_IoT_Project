from flask import request
from flask_restful import Resource

from static.py.bbdd import DatabaseManager

db = DatabaseManager()

'''
EJEMPLO DE REQUEST
{
    'rain' : [
        {
            "rain_detected": bool,
            "intensity": float,
            "timestamp": string
        },
        ...,
        {
            "rain_detected": bool,
            "intensity": float,
            "timestamp": string
        }
    ],
    'temperature' : [
        {
            "temperature": float,
            "humidity": float,
            "timestamp": string
        },
        {
            "temperature": float,
            "humidity": float,
            "timestamp": string
        },
        {
            "temperature": float,
            "humidity": float,
            "timestamp": string
        }
    ],
    'motion' : [
        {
            "motion_detected": bool,
            "timestamp": string
        }
    ],
    'pressure' : [
        {
            "pressure": float,
            "altitude": float,
            "timestamp": string
        }
    ]
}
'''

# Clase para manejar el recurso
class Endpoint_ESP32(Resource):

    def get(self):
        try:
            # ===== Consulta BD
            rain_data = db.fetch_all("SELECT * FROM rain;")
            temperature_data = db.fetch_all("SELECT * FROM temperature;")
            motion_data = db.fetch_all("SELECT * FROM motion;")
            pressure_data = db.fetch_all("SELECT * FROM pressure;")

            # ===== Confirmación
            return {"status":"fetched!","data":{
                "rain":rain_data,
                "temperature":temperature_data,
                "motion":motion_data,
                "pressure":pressure_data,
            }}, 200
        
        # ===== Manejor de errores
        except KeyError as ex: return {"status":"failed!","reason":f"The key {ex} was not in request."}, 400

        except Exception as ex: return {"status":"failed!","reason":f"{ex}"}, 500
   
    def post(self):
        try:
            # ===== Validacion de datos
            data = dict(request.json)
            
            # ===== Obtencion de valores
            rain_data        = data['rain']
            temperature_data = data['temperature']
            motion_data      = data['motion']
            pressure_data    = data['pressure']

            # ===== Guardar información
            db.insert_data('rain',rain_data)
            db.insert_data('temperature',temperature_data)
            db.insert_data('motion',motion_data)
            db.insert_data('pressure',pressure_data)

            # ===== Confirmacion
            return {"status": "Data Updated" }, 201
    
        # ===== Manejor de errores
        except KeyError as ex: return {"status":"failed!","reason":f"The key {ex} was not in request."}, 400

        except Exception as ex: return {"status":"failed!","reason":f"{ex}"}, 500

    def delete(self):
        try:
            # ===== Validacion de datos
            data = dict(request.json)
            data_keys = data.keys()
            
            # ===== Obtencion de valores
            tabla      = data['table']
            start_date = data['start_date']
            end_date   = data['end_date']

            # ===== Procesamiento de solicitud
            db.delete_records(tabla,start_date,end_date)
            
            # ===== Confirmación
            return {"status":"Data successfully deleted!"}, 200

        # ===== Manejor de errores
        except KeyError as ex: return {"status":"failed!","reason":f"The key {ex} was not in request."}, 400

        except Exception as ex: return {"status":"failed!","reason":f"{ex}"}, 500