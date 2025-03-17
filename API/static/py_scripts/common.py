from datetime import datetime, timedelta
import os
import threading
import time

last_called = datetime.now()
check = None
print('wtf desde common')

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