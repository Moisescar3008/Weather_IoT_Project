import os, sys
from datetime import datetime
from flask import Flask, render_template
from flask_restful import Api
from flask_cors import CORS

from static.py_scripts.Endpoints.sensores import ESP32_HTTP, ESP32_MQTT
from static.py_scripts.bbdd import DatabaseManager

DatabaseManager().start_connection()

app = Flask(__name__)
CORS(app)
api = Api(app)
sys.stdout = sys.stderr

# ===== Interfaz
@app.route('/')
def home():
    global last_called

    # ===== Obtención de datos
    data = ESP32_HTTP()
    data = data.get()[0]['data']
    
    temp = data.get('temperature', None)
    rain = data.get('rain', None)
    moti = data.get('motion', None)
    pres = data.get('pressure', None)

    # Actualiza la hora de la última llamada
    last_called = datetime.now()

    return render_template(
        'index.html',
        temp=temp,
        rain=rain,
        moti=moti,
        pres=pres
    )

# ===== Endpoints
api.add_resource(ESP32_HTTP, "/html/sensores")


if __name__ == '__main__':
    # os.system('clear')

    app.run(debug=True, host="0.0.0.0", port=10000)
