from flask import Flask
from SystemMonitoring import SystemMonitor

app = Flask(__name__)

systemMonitoring = SystemMonitor()

@app.route('/')
def get_system_information():
    return systemMonitoring.get_system_information()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9636, debug=True)
