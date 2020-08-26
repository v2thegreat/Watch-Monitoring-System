from time import sleep
from datetime import datetime
from pymongo import MongoClient
from SystemMonitoring import SystemMonitor
from config.config import config_obj

client = MongoClient(f'mongodb://{config_obj["database"]["host"]}:{config_obj["database"]["port"]}')
db = client.SystemMonitoringDatabase.SystemMonitoringDatabase

systemMonitoring = SystemMonitor()

if __name__ == '__main__':
    while True:
        current_datetime = datetime.now()
        sys_info = systemMonitoring.get_system_information()
        sys_info['datetime'] = current_datetime
        try:
            db.insert_one(sys_info)
        except Exception as e: #TODO: Add more verbosity for exceptions
            print(f"Exception: {e} was raised, skipping for this ping")
        else:
            print(f'Saved data at: {current_datetime}')
        sleep(10)
