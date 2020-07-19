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
        sys_info = systemMonitoring.get_system_information()
        sys_info['datetime'] = datetime.now()
        db.insert_one(sys_info)
        sleep(10)