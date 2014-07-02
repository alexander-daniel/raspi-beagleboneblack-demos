import plotly.plotly as py
from plotly.graph_objs import *
import json
import time
import datetime
import Adafruit_BMP.BMP085 as BMP085

# Default constructor will pick a default I2C bus.
#
# For the Raspberry Pi this means you should hook up to the only exposed I2C bus
# from the main GPIO header and the library will figure out the bus number based
# on the Pi's revision.
#
# For the Beaglebone Black the library will assume bus 1 by default, which is
# exposed with SCL = P9_19 and SDA = P9_20.
sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)

# Optionally you can override the bus number:
#sensor = BMP085.BMP085(busnum=2)

# You can also optionally change the BMP085 mode to one of BMP085_ULTRALOWPOWER, 
# BMP085_STANDARD, BMP085_HIGHRES, or BMP085_ULTRAHIGHRES.  See the BMP085
# datasheet for more details on the meanings of each mode (accuracy and power
# consumption are primarily the differences).  The default mode is STANDARD.
#sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)



username = 'workshop'
api_key = 'v6w5xlbx9j'
stream_tokens = ['25tm9197rz','unbi52ww8a','ibsfyg7qd8','t3ugglls9r']
stream_server = 'http://stream.plot.ly'

py.sign_in(username, api_key)

temperature_trace = Scatter(x=[],
                      y=[],
                      mode='lines+markers',
                      name='Temperature (C)',
                      yaxis='y1',
                      stream=dict(
                        token=stream_tokens[0],
                        maxpoints=3600)
                        )

pressure_trace = Scatter(x=[],
                      y=[],
                      mode='lines+markers',
                      name='Pressure (P)',  
                      yaxis='y2',
                      stream=dict(
                        token=stream_tokens[1],
                        maxpoints=3600)
                        )

altitude_trace = Scatter(x=[],
                      y=[],
                      mode='lines+markers',
                      name='Altitude (M)',  
                      yaxis='y3',
                      stream=dict(
                        token=stream_tokens[2],
                        maxpoints=3600)
                        )

sealevel_pressure_trace = Scatter(x=[],
                      y=[],
                      mode='lines+markers',
                      name='SeaLevel Pressure',  
                      yaxis='y4',
                      stream=dict(
                        token=stream_tokens[3],
                        maxpoints=3600)
                        )

# Package them into data object
data = Data([temperature_trace, pressure_trace, altitude_trace, sealevel_pressure_trace])

# Layout object
layout = Layout(title='Streaming BMP180 Subplots',  # plot's title
                   yaxis1= YAxis(domain=[0.0, 0.2]),       #  and range
                   yaxis2= YAxis(domain=[0.25, 0.45]),
                   yaxis3= YAxis(domain=[0.5, 0.7]),
                   yaxis4= YAxis(domain=[0.75, 0.95])
                  )

figure = Figure(data=data, layout=layout)

print py.plot(figure, filename='BMP180 Raspi Streaming Subplots')

# create some stream objects for your traces
temperature_stream = py.Stream(stream_tokens[0])
pressure_stream = py.Stream(stream_tokens[1])
altitude_stream = py.Stream(stream_tokens[2])
sealevel_pressure_stream = py.Stream(stream_tokens[3])

#open the streams!
temperature_stream.open()
pressure_stream.open()
altitude_stream.open()
sealevel_pressure_stream.open()

#the main sensor reading loop
while True:
    date_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

    temperature_stream.write({
        'x': date_stamp,
        'y': sensor.read_temperature()
    })

    pressure_stream.write({
        'x': date_stamp,
        'y': sensor.read_pressure()
    })

    altitude_stream.write({
        'x': date_stamp,
        'y': sensor.read_altitude()
    })

    sealevel_pressure_stream.write({
        'x': date_stamp,
        'y': sensor.read_sealevel_pressure()
    })

    print 'Temp = {0:0.2f} *C'.format(sensor.read_temperature())
    print 'Pressure = {0:0.2f} Pa'.format(sensor.read_pressure())
    print 'Altitude = {0:0.2f} m'.format(sensor.read_altitude())
    print 'Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure())


    # delay between stream posts
    time.sleep(1)
