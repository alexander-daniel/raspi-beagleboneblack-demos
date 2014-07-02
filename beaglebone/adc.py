import Adafruit_BBIO.ADC as ADC
ADC.setup()

#read returns values 0-1.0
value = ADC.read("P9_40")

#read_raw returns non-normalized value
value = ADC.read_raw("P9_40")
