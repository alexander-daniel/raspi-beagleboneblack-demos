import plotly.plotly as py
import time
import readadc
import datetime

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
        'maxpoints': 200
    }}],
    filename='Raspberry Pi Streaming Example Values',
    fileopt='overwrite')

# temperature sensor connected channel 0 of mcp3008
sensor_pin = 0
readadc.initialize()

stream = py.Stream(stream_token)
stream.open()

#the main sensor reading loop
while True:
    date_stamp = datetime.datetime.now()
    sensor_data = readadc.readadc(sensor_pin,
                                  readadc.PINS.SPICLK,
                                  readadc.PINS.SPIMOSI,
                                  readadc.PINS.SPIMISO,
                                  readadc.PINS.SPICS)

    millivolts = sensor_data * (3300.0 / 1023.0)
    temp_C = ((millivolts - 100.0) / 10.0) - 40.0
    #temp_F = ( temp_C * 9.0 / 5.0 ) + 32

    stream.write({
        'x': date_stamp.strftime('%Y-%m-%d %H:%M:%S.%f'),
        'y': temp_C
    })

    # delay between stream posts
    time.sleep(0.25)
