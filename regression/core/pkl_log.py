import os
import pickle
from datetime import datetime

LOG_PATH_PKL = os.path.join(os.path.dirname(__file__), "/app/log.pkl")

def write_log_pkl(text):
    log_entry = {
        "timestamp": datetime.now(),
        "message": text
    }

    logs = []

    # Leer archivo si existe
    if os.path.exists(LOG_PATH_PKL):
        try:
            with open(LOG_PATH_PKL, "rb") as f:
                logs = pickle.load(f)
        except Exception as e:
            print(f"Error leyendo logs: {e}")
            logs = []

    # Añadir nuevo log y guardar
    logs.append(log_entry)

    try:
        with open(LOG_PATH_PKL, "wb") as f:
            pickle.dump(logs, f)
    except Exception as e:
        print(f"Error escribiendo logs: {e}")
