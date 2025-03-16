from flask import Flask, render_template
from flask_restful import Api
from flask_cors import CORS

from static.py.sensores import ESP32_HTTP, ESP32_MQTT

app = Flask(__name__)
CORS(app)
api = Api(app)  # Crear la API

# ===== Interfaz
@app.route('/')
def home():

    # ===== Obtencion de datos
    data = ESP32_HTTP()
    data = data.get()[0]['data']
    
    temp = data.get('temperature',None)
    rain = data.get('rain',None)
    moti = data.get('motion',None)
    pres = data.get('pressure',None)


    return render_template(
        'index.html',
        temp = temp,
        rain = rain,
        moti = moti,
        pres = pres,
    )

# ===== Endpoints
api.add_resource(ESP32_HTTP, "/html/sensores")
api.add_resource(ESP32_MQTT, "/mqtt/sensores")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=10000)
