import random
import time
from datetime import datetime
import json

def generate_data():
    temperature_values =[]
    pressure_values = []
    rain_values = []
    motion_values = []
    start = time.time()
    while (time.time() - start) < 1:
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
        'rain': rain_values,
        'temperature': temperature_values,
        'motion': motion_values,
        'pressure': pressure_values
    }

    with open("iot.json", "w") as outfile:
        return json.dump(values, outfile)

if __name__  == "__main__":
    values = generate_data()
