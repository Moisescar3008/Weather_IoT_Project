import random
import time
from datetime import datetime
import json
import paho.mqtt.client as mqtt

# Configuración del broker
BROKER = "172.17.0.1"  # Cambia esto si usas un broker remoto
PORT = 10001
TOPIC = "esp32/data"
INTERVALO = 5  # Intervalo de tiempo en segundos

def generate_data():
    temperature_values = []
    pressure_values = []
    rain_values = []
    motion_values = []
    
    boolean = random.choice(["True", "False"])
    rain = random.choice([0, 1])
    current = datetime.now().replace(microsecond=0)
    
    temperature_humidity_data = {
        "temperature": random.uniform(7, 60),
        "humidity": random.uniform(0, 100),
        "timestamp": f"{current}"
    }
    pressure_altitude_data = {
        "pressure": random.uniform(880, 1080),
        "altitude": random.uniform(0, 500),
        "timestamp": f"{current}"
    }
    rain_data = {
        "rain_detected": rain,
        "intensity": random.uniform(-50, 100),
        "timestamp": f"{current}"
    }
    motion_data = {
        "motion_detected": boolean,
        "timestamp": f"{current}"
    }

    temperature_values.append(temperature_humidity_data)
    pressure_values.append(pressure_altitude_data)
    rain_values.append(rain_data)
    motion_values.append(motion_data)

    values = {
        'action':'post',
        'rain': rain_values,
        'temperature': temperature_values,
        'motion': motion_values,
        'pressure': pressure_values
    }
    
    return json.dumps(values)

def on_connect(client, userdata, flags, rc):
    print(f"Conectado con código de resultado {rc}")

if __name__  == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(BROKER, PORT, 60)
    
    client.loop_start()
    
    try:
        while True:
            data = generate_data()
            client.publish(TOPIC, data)
            print(f"\nDatos enviados al tópico '{TOPIC}': {data}")
            time.sleep(INTERVALO)  # Espera antes de enviar nuevamente
    except KeyboardInterrupt:
        print("Interrumpido por el usuario. Desconectando...")
    
    client.loop_stop()
    client.disconnect()
