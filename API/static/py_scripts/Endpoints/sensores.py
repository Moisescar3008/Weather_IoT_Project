import os,sys,json
from flask import request
from flask_restful import Resource
import paho.mqtt.client as mqtt

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from bbdd import DatabaseManager

db        = DatabaseManager()
BROKER    = "mqtt_broker"
PORT      = 1883
TOPIC_SUB = "esp32/data"
TOPIC_PUB = "esp32/response"

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


class ESP32_HTTP(Resource):

    def get(self):
        try:
            # ===== Validacion de datos
            data = dict(request.json) if request.is_json else dict()
            
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



class ESP32_MQTT(Resource):
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(BROKER, PORT, 60)
        # self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Conectado con éxito al broker")
            client.subscribe(TOPIC_SUB)
        else:
            print(f"Error de conexión con código: {rc}")


    def on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
            print(f"📩 Mensaje recibido en '{msg.topic}': {data}")
            action = data.get("action")
            
            if action == "post": response = self.post(data)
            else:                response = {"status": "failed!", "reason": "Invalid action."}
            
            client.publish(TOPIC_PUB, json.dumps(response))
        except Exception as ex:
            print(f"❌ Error procesando mensaje: {ex}")
            client.publish(TOPIC_PUB, json.dumps({"status": "failed!", "reason": str(ex)}))


    def post(self, data):
        try:
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

            return {"status": "Data Updated"}
        except Exception as ex:
            return {"status": "failed!", "reason": str(ex)}
