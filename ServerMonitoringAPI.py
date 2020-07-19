from pymongo import MongoClient
import pandas as pd
from pandas import json_normalize
from flask import Flask

from SystemMonitoring import get_size
from config.config import config_obj

app = Flask(__name__)
client = MongoClient(f'mongodb://{config_obj["database"]["host"]}:{config_obj["database"]["port"]}')
db = client.SystemMonitoringDatabase.SystemMonitoringDatabase


@app.route('/minimal')
def get_system_information_minimal():
    data = [x for x in db.find()]
    data_dataframe = pd.DataFrame(data)
    cpu = json_normalize(data_dataframe['cpu'])
    memory = json_normalize(data_dataframe['memory'])
    disk = json_normalize(data_dataframe['disk'])
    network = json_normalize(data_dataframe['network'])

    return {
        'cpu': cpu.aggregate('mean')['total_core_usage'],
        'memory': memory.aggregate('mean')['percentageMemory'],
        'diskRead': get_size(disk['read'].aggregate('mean')),
        'diskWrite': get_size(disk['write'].aggregate('mean')),
        'networkSent': get_size(network['sent'].aggregate('mean')),
        'networkReceived': get_size(network['received'].aggregate('mean'))
    }


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config_obj['monitoringServer']['port'], debug=True)
