import plotly.plotly as py
import json
import time
import readadc

# Fill in the config.json file in this directory with your plotly username,
# plotly API key, and your generated plotly streaming tokens
# Sign up to plotly here: https://plot.ly/ssu
# View your API key and streaming tokens here: https://plot.ly/settings

with open('./config.json') as config_file:
    plotly_user_config = json.load(config_file)

username = 'workshop'
api_key = 'v6w5xlbx9j'
stream_token = '25tm9197rz'
stream_server = 'http://stream.plot.ly'

py.sign_in(username, api_key)

print p.plot([{'x': [], 'y': [], 'type': 'scatter',
            'stream': {'token': stream_token, 'maxpoints': 200}
          }], filename='Raspberry Pi Streaming Example Values', fileopt='overwrite')

stream = py.Stream(stream_token)
stream.open()

#the main sensor reading loop
while True:
		sensor_data = readadc.readadc(sensor_pin, readadc.PINS.SPICLK, readadc.PINS.SPIMOSI, readadc.PINS.SPIMISO, readadc.PINS.SPICS)
		stream.write({'x': i, 'y': sensor_data })
		i+=1
		# delay between stream posts
		time.sleep(0.25)
