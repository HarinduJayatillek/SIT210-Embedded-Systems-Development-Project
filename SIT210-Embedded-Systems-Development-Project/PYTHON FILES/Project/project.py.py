#import libraries
import RPi.GPIO as GPIO
import dht11
import time
import paho.mqtt.publish as publish
import os
from twilio.rest import Client
import datetime
import time
import Adafruit_CharLCD as LCD
import telepot
from telepot.loop import MessageLoop

c = 1

date = datetime.datetime.now()

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
sensor_outside = 4
lcd_rs = 26
lcd_en = 19
lcd_d4 = 13
lcd_d5 = 6
lcd_d6 = 5
lcd_d7 = 11
lcd_backlight = 4
lcd_columns = 16
lcd_row = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_row, lcd_backlight)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

instance = dht11.DHT11(sensor_outside)

def mainLogic():

	while True:

			global c

			#sensor reading data
			result = instance.read()
			time.sleep(5)

			#continue if the data are valid
			if result.is_valid():

				print("Date: "+str(date))
				print("Temperature: %d C" % result.temperature +' '+ "Humidity: %d %%" % result.humidity)
				print("\n")

				tempLcd = result.temperature
				humLcd = result.humidity

				lcd.clear()
				lcd.message(str(date))
				lcd.message("\nTemperature: %dC" % tempLcd)
				time.sleep(1)

				def action(msg):

		                        chat_id = msg['chat']['id']
		                        command = msg['text']
		                	print('Received: %s' % command)

					command = command.lower()
		                        if command == "temp":
						telegram_bot.sendMessage(chat_id, str("Temperature: ")+str(result.temperature)+" C")

					elif command == "hum":
						telegram_bot.sendMessage(chat_id, str("Humidity: ")+str(result.humidity)+"%")

					elif command == "weather":
						telegram_bot.sendMessage(chat_id, str("Temperature: ")+str(result.temperature)+" C")
						telegram_bot.sendMessage(chat_id, str("Humidity: ")+str(result.humidity)+"%")

					elif command == "acon" or command == "ac on":
						publish.single("MyWeather/ac", "ac", hostname="test.mosquitto.org")
	                                        print("Ac turned on\n")
                	                        time.sleep(1)

					elif command == "heateron" or command == "heater on":
	                                        publish.single("MyWeather/heater", "heat", hostname="test.mosquitto.org")
	                                        print("Heater turned on\n")
	                                        time.sleep(1)

					elif command == "bothoff" or command == "both off":
	                                        publish.single("MyWeather/both", "both", hostname="test.mosquitto.org")
	                                        print("Both AC and heater turned off\n")
	                                        time.sleep(1)


			#teleBot Opration
			if (c == 1):
				telegram_bot = telepot.Bot('1184248171:AAHneWUXeVsNRlpZ74Vgyd35K4BOzjzC7_A')
				print(telegram_bot.getMe())

				MessageLoop(telegram_bot, action).run_as_thread()
				print('Up and Running')
				c = c + 1


mainLogic()

time.sleep(5)
GPIO.cleanup()
