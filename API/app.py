from flask import Flask, render_template, request, jsonify
from flask_restful import Api, Resource

from static.py.endpoints import Endpoint_ESP32

app = Flask(__name__)
api = Api(app)  # Crear la API

# ===== Interfaz
@app.route('/')
def home():

    # ===== Obtencion de datos
    data = Endpoint_ESP32()
    data = data.get()[0]['data']
    
    temp = data['temperature']
    rain = data['rain']
    moti = data['motion']
    pres = data['pressure']


    return render_template(
        'index.html',
        temp = temp,
        rain = rain,
        moti = moti,
        pres = pres,
    )

# ===== Endpoints
api.add_resource(Endpoint_ESP32, "/api/sensores")

if __name__ == '__main__':
    app.run(debug=True)
