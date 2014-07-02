import Adafruit_BBIO.ADC as ADC
import plotly.plotly as py
import datetime
import time

# Fill in the config.json file in this directory with your plotly username,
# plotly API key, and your generated plotly streaming tokens
# Sign up to plotly here: https://plot.ly/ssu
# View your API key and streaming tokens here: https://plot.ly/settings

username = 'workshop'
api_key = 'v6w5xlbx9j'
stream_token = '25tm9197rz'
stream_server = 'http://stream.plot.ly'

py.sign_in(username, api_key)

print py.plot([{
    'x': [],
    'y': [],
    'type': 'scatter',
    'stream': {
        'token': stream_token,
        'maxpoints': 20000}}],
    filename='BBB UV Sensor Streaming',
    fileopt='overwrite')

# temperature sensor connected to pin P9_40
UV_pin = 'P9_40'
REF_pin = 'P9_39'

ADC.setup()

stream = py.Stream(stream_token)
stream.open()

while True:

    uv_reading = ADC.read(UV_pin)
    ref_reading = ADC.read(REF_pin)
    outputVoltage = 3.3 / refLevel * uvLevel;
    uvIntensity = mapfloat(outputVoltage, 0.99, 2.8, 0.0, 15.0)
    
    date_stamp = datetime.datetime.now()

    stream.write({
        'x': date_stamp.strftime('%Y-%m-%d %H:%M:%S.%f'),
        'y': uvIntensity 
    })
    print uvIntensity

    time.sleep(0.05)



def mapfloat(x, in_min, in_max, out_min, out_max):

  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
