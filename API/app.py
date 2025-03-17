from flask import Flask, render_template, request
from flask_restful import Api
from flask_cors import CORS
from datetime import datetime, timedelta
import os
import threading
import time

from static.py_scripts.Endpoints.sensores import ESP32_HTTP, ESP32_MQTT

app = Flask(__name__)
CORS(app)
api = Api(app)

# Variable global para almacenar la hora de la última llamada
last_called = datetime.now()
check = False

def check_time_repeatedly():
    ''' Función para verificar cada 5 segundos si han pasado 5 minutos desde la última solicitud '''
    global last_called, check
    print(f"Dentro de bucle last_called: {last_called}")
    while True:
        print(f"\tDentro de bucle: {check}")
        if check:
            current_time = datetime.now()
            print(f"\t\tcurrent_time: {current_time}")
            print(f"\t\tlast_called: {last_called}")
            if (current_time - last_called) > timedelta(seconds=5):
                print(f"Han pasado 15 segundos desde la última solicitud: {last_called}")
                last_called = current_time  # Actualiza la última llamada
            check = False
        time.sleep(5)

# ===== Middleware: se ejecuta después de cada solicitud
@app.after_request
def after_request(response):
    global last_called, check

    print(f"\tSe hizo una peticion, esto es lo que se ejcuta después")
    print(f"\t\t(A) last_called: {last_called}\n\t\t(A) check: {check}")

    last_called = datetime.now()
    check = True
    print(f"\t\t(D) last_called: {last_called}\n\t\t(D) check: {check}")

    return response

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
api.add_resource(ESP32_MQTT, "/mqtt/sensores")

if __name__ == '__main__':
    os.system('clear')

    # Arranca el hilo en segundo plano al iniciar la aplicación
    thread = threading.Thread(target=check_time_repeatedly)
    thread.daemon = True  # Esto permite que el hilo se termine cuando se cierre la aplicación
    thread.start()

    app.run(debug=True, host="0.0.0.0", port=10000)
