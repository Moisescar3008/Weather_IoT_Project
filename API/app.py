from flask import Flask, render_template, request, jsonify
from flask_restful import Api, Resource

from static.py.humedad import Endpoint_Sensor_Humedad

app = Flask(__name__)
api = Api(app)  # Crear la API



# ===== Interfaz
@app.route('/')
def home():
    return render_template('index.html')

# ===== Endpoints
api.add_resource(Endpoint_Sensor_Humedad, "/api/sensores/humedad")

if __name__ == '__main__':
    app.run(debug=True)
