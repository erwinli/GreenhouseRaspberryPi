from pubnub import Pubnub
import os 
import json 
import subprocess
import RPi.GPIO as GPIO
import time
from pyrebaseInit import Pyrebase

GPIO.setmode(GPIO.BCM)
firebase = Pyrebase("AIzaSyDwotenCiGA0gdyjiyQQRedwfbfe-1Xuz4", "greenhouse-b8aec.firebaseapp.com", "https://greenhouse-b8aec.firebaseio.com/", "greenhouse-b8aec.appspot.com")

# Pin Mapping:
# 16 = Solenoid
# 18 = Float sensor

def router(message, channel):
	solenoidPin = 16
	fanPin = 12

	if type(message) == dict:
		try:
			if channel == "command":
				if message["message"] == "solenoid":
					if message["value"] == "open":
						toggle_solenoid_on(solenoidPin)
					else:
						toggle_solenoid_off(solenoidPin)
				elif message["message"] == "fan":
					if message["value"] == "on":
						toggle_fan_on(fanPin)
					else:
						toggle_fan_off(fanPin)
				else:
					error(message)
		except ValueError, e:
			print ("Failed.")
	else:
		error(message)
		
def publish_data(value, type):
	if(type == "solenoid" and value == "open"):
		firebase.logSolenoidOn()
	elif(type == "solenoid" and value == "closed"):
		firebase.logSolenoidOff()
	elif(type == "fan" and value == "on"):
		firebase.logFanOn()
	elif(type == "fan" and value == "off"):
		firebase.logFanOff()
	elif(type == "float" and value == "full"):
		firebase.logWaterTankIsFull()
	elif(type == "float" and value == "empty"):
		firebase.logWaterTankNotFull()
		
def toggle_solenoid_on(pin):
	print("Fan On")
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.HIGH)
	publish_data("open", "solenoid")
	
def toggle_solenoid_off(pin):
	print("Fan Off")
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.LOW)
	publish_data("closed", "solenoid")	

def toggle_fan_on(pin):
	print("Fan On")
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.HIGH)
	publish_data("on", "fan")
	
def toggle_fan_off(pin):
	print("Fan Off")
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.LOW)
	publish_data("off", "fan")

def is_water_level_full(pin):
	GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	floatSensor = GPIO.input(pin)
	if(floatSensor == True):
		return True
	else:
		return False

floatPin = 18
floatStatus = 0
while True:
	if(is_water_level_full(floatPin) and floatStatus == 0):
		publish_data("full", "float")
		floatStatus = 1
		print('full')
	elif(not is_water_level_full(floatPin) and floatStatus == 1):
		publish_data("empty", "float")
		floatStatus = 0
		print('empty')

