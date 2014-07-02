import Adafruit_BBIO.ADC as ADC
import plotly.plotly as py
import datetime
import time

# Fill in the config.json file in this directory with your plotly username,
# plotly API key, and your generated plotly streaming tokens
# Sign up to plotly here: https://plot.ly/ssu
# View your API key and streaming tokens here: https://plot.ly/settings

username = 'demos'
api_key = 'tj6mr52zgp'
stream_token = 'lu1xzzrt70'
stream_server = 'http://stream.plot.ly'

py.sign_in(username, api_key)

print py.plot([{
    'x': [],
    'y': [],
    'type': 'scatter',
    'stream': {
        'token': stream_token,
        'maxpoints': 20000}}],
    filename='BBB Liquid Level Streaming',
    fileopt='overwrite')

# temperature sensor connected to pin P9_40
sensor_pin = 'P9_40'

ADC.setup()

stream = py.Stream(stream_token)
stream.open()

SERIESRESISTOR = 10000

while True:

    reading = ADC.read(sensor_pin) - 1
    
    reading = SERIESRESISTOR / reading;
    print reading
    
    date_stamp = datetime.datetime.now()

    stream.write({
        'x': date_stamp.strftime('%Y-%m-%d %H:%M:%S.%f'),
        'y': reading 
    })

    time.sleep(0.05)
