import os
import time
from flask import Flask, request, jsonify, render_template
from AirQualityMonitor import AirQualityMonitor
from apscheduler.schedulers.background import BackgroundScheduler
import redis
import atexit
from flask_cors import CORS, cross_origin
from audio_player import AudioPlayer


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
aqm = AirQualityMonitor()
player = AudioPlayer(volume=90)


def aqi_alert(aqi_limit=20):
    current_measurement = aqm.get_measurement()
    aqi = current_measurement['measurement']['aqi']
    if aqi > aqi_limit:
        print(f"AQI Alert! Current AQI is {aqi}")
        player.play_audio()
    else:
        print('AQI is below threshold... continuing')


scheduler = BackgroundScheduler()
scheduler.add_job(func=aqm.save_measurement_to_redis, trigger="interval", seconds=60)
scheduler.add_job(func=aqi_alert, trigger="interval", seconds=10)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())


def pretty_timestamps(measurement):
    timestamps = []
    for x in measurement:
        timestamp = x['measurement']['timestamp']
        timestamps += [timestamp.split('.')[0]]
    return timestamps

def reconfigure_data(measurement):
    """Reconfigures data for chart.js"""
    current = int(time.time())
    measurement = measurement[:30]
    measurement.reverse()
    return {
        'labels': pretty_timestamps(measurement),
        'aqi': {
            'label': 'aqi',
            'data': [x['measurement']['aqi'] for x in measurement],
            'backgroundColor': '#181d27',
            'borderColor': '#181d27',
            'borderWidth': 3,
        },
        'pm10': {
            'label': 'pm10',
            'data': [x['measurement']['pm10'] for x in measurement],
            'backgroundColor': '#cc0000',
            'borderColor': '#cc0000',
            'borderWidth': 3,
        },
        'pm2': {
            'label': 'pm2.5',
            'data': [x['measurement']['pm2.5'] for x in measurement],
            'backgroundColor': '#42C0FB',
            'borderColor': '#42C0FB',
            'borderWidth': 3,
        },
    }

@app.route('/')
def index():
    """Index page for the application"""
    context = {
        'historical': reconfigure_data(aqm.get_last_n_measurements()),
    }
    return render_template('index.html', context=context)


@app.route('/api/')
@cross_origin()
def api():
    """Returns historical data from the sensor"""
    context = {
        'historical': reconfigure_data(aqm.get_last_n_measurements()),
    }
    return jsonify(context)


@app.route('/api/now/')
def api_now():
    """Returns latest data from the sensor"""
    context = {
        'current': aqm.get_measurement(),
    }
    return jsonify(context)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=int(os.environ.get('PORT', '8000')))
