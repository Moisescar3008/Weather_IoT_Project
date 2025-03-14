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
            # ===== Validacion de datos
            data = dict(request.json)
            
            # ===== Obtencion de valores
            table = data.get('table',None)
            if not(table): tables = ['rain','temperature','motion','pressure']
            else:          tables = [table,]

            # ===== Consulta BD
            result = {}
            for table in tables:
                fetch = db.fetch_all(f"SELECT * FROM {table};")
                result[table] = fetch                

            # ===== Confirmación
            return {"status":"fetched!","data":result}, 200
        
        # ===== Manejor de errores
        except KeyError as ex: return {"status":"failed!","reason":f"The key {ex} was not in request."}, 400

        except Exception as ex: return {"status":"failed!","reason":f"{ex}"}, 500
   
    def post(self):
        try:
            # ===== Validacion de datos
            data = dict(request.json)
            
            # ===== Obtencion de valores
            rain_data        = data.get('rain',[])
            temperature_data = data.get('temperature',[])
            motion_data      = data.get('motion',[])
            pressure_data    = data.get('pressure',[])

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
            
            # ===== Obtencion de valores
            tabla      = data.get('table',None)
            start_date = data.get('start_date',None)
            end_date   = data.get('end_date',None)

            # ===== Procesamiento de solicitud
            db.delete_records(tabla,start_date,end_date)
            
            # ===== Confirmación
            return {"status":"Data successfully deleted!"}, 200

        # ===== Manejor de errores
        except KeyError as ex: return {"status":"failed!","reason":f"The key {ex} was not in request."}, 400

        except Exception as ex: return {"status":"failed!","reason":f"{ex}"}, 500