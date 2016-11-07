import pyrebase
import datetime
import json
from time import gmtime, strftime

config = {
	"apiKey" : "AIzaSyDwotenCiGA0gdyjiyQQRedwfbfe-1Xuz4",
	"authDomain" : "greenhouse-b8aec.firebaseapp.com",
	"databaseURL" : "https://greenhouse-b8aec.firebaseio.com/",
	"storageBucket" : "greenhouse-b8aec.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

# Used to convert datetime object into UTC date format
def convertDatetimeToUTC(dateTime):
	UTCDateTime = (dateTime - datetime.datetime(1970, 1, 1)).total_seconds()
	return UTCDateTime

# writes to firebase table sensor/photocell with the current date and inputted value
def writeToPhotocellTable(value):
	data = {
		"value" : value,
		"datetime" : convertDatetimeToUTC(datetime.datetime.now())
	}
	db.child("sensor").child("photocell").push(data)

# writes to firebase table sensor/humidity with the current date and inputted value
def writeToHumidityTable(value):
	data = {
		"value" : value,
		"datetime" : convertDatetimeToUTC(datetime.datetime.now())
	}
	db.child("sensor").child("humidity").push(data)

# writes to firebase table sensor/tempurature with the current date and inputted value
def writeToTempuratureTable(value):
	data = {
		"value" : value,
		"datetime" : convertDatetimeToUTC(datetime.datetime.now())
	}
	db.child("sensor").child("tempurature").push(data)

# writes to firebase table sensor/soil with the current date and inputted value
def writeToSoilTable(value):
	data = {
		"value" : value,
		"datetime" : convertDatetimeToUTC(datetime.datetime.now())
	}
	db.child("sensor").child("soil").push(data)

def logFanOn():
	data = {
		"value" : 1,
		"datetime" : convertDatetimeToUTC(datetime.datetime.now())
	}
	db.child("motor").child("fan").push(data)

def logFanOff():
	data = {
		"value" : 0,
		"datetime" : convertDatetimeToUTC(datetime.datetime.now())
	}
	db.child("motor").child("fan").push(data)

def logSolenoidOn():
	data = {
		"value" : 1,
		"datetime" : convertDatetimeToUTC(datetime.datetime.now())
	}
	db.child("solenoid").child("solenoid").push(data)

def logSolenoidOff():
	data = {
		"value" : 0,
		"datetime" : convertDatetimeToUTC(datetime.datetime.now())
	}
	db.child("solenoid").child("solenoid").push(data)

# TODO save all reading values into array

def readPhotocellDataFromDateRange(seconds = 0, minutes = 0, hours = 0, days = 0):
	endDateRange = datetime.datetime.now()
	startDateRange = endDateRange - datetime.timedelta(seconds=seconds) - datetime.timedelta(minutes=minutes) - datetime.timedelta(hours=hours) - datetime.timedelta(days=days)
	
	photocellReadings = db.child("sensor").child("photocell").order_by_child("datetime").start_at(convertDatetimeToUTC(startDateRange)).end_at(convertDatetimeToUTC(endDateRange)).get()

	for photocellReading in photocellReadings.each():
		photocellValue = photocellReading.val()
		print photocellValue["value"]

def readHumidityDataFromDateRange(seconds = 0, minutes = 0, hours = 0, days = 0):
	endDateRange = datetime.datetime.now()
	startDateRange = endDateRange - datetime.timedelta(seconds=seconds) - datetime.timedelta(minutes=minutes) - datetime.timedelta(hours=hours) - datetime.timedelta(days=days)
	
	humidityReadings = db.child("sensor").child("humidity").order_by_child("datetime").start_at(startDateRange).end_at(endDateRange).get()

	for humidityReading in humidityReadings.each():
		humidityValue = humidityReading.val()
		print humidityValue["value"]

def readTempuratureDataFromDateRange(seconds = 0, minutes = 0, hours = 0, days = 0):
	endDateRange = datetime.datetime.now()
	startDateRange = endDateRange - datetime.timedelta(seconds=seconds) - datetime.timedelta(minutes=minutes) - datetime.timedelta(hours=hours) - datetime.timedelta(days=days)
	
	tempuratureReadings = db.child("sensor").child("tempurature").order_by_child("datetime").start_at(startDateRange).end_at(endDateRange).get()

	for tempuratureReading in tempuratureReadings.each():
		tempuratureValue = tempuratureReading.val()
		print tempuratureValue["value"]

def readSoilDataFromDateRange(seconds = 0, minutes = 0, hours = 0, days = 0):
	endDateRange = datetime.datetime.now()
	startDateRange = endDateRange - datetime.timedelta(seconds=seconds) - datetime.timedelta(minutes=minutes) - datetime.timedelta(hours=hours) - datetime.timedelta(days=days)
	
	soilReadings = db.child("sensor").child("soil").order_by_child("datetime").start_at(startDateRange).end_at(endDateRange).get()

	for soilReading in soilReadings.each():
		soilValue = soilReading.val()
		print soilValue["value"]

# reads x amount of latest entries
def readLatestPhotocellData(amount = 0):
	photocellReadings = db.child("sensor").child("photocell").limit_to_first(amount).get()

	for photocellReading in photocellReadings.each():
		photocellValue = photocellReading.val()
		print photocellValue["value"]

def readLatestHumidityData(amount = 0):
	humidityReadings = db.child("sensor").child("humidity").limit_to_first(amount).get()

	for humidityReading in humidityReadings.each():
		humidityValue = humidityReading.val()
		print humidityValue["value"]

def readLatestTempuratureData(amount = 0):
	tempuratureReadings = db.child("sensor").child("tempurature").limit_to_first(amount).get()

	for tempuratureReading in tempuratureReadings.each():
		tempuratureValue = tempuratureReading.val()
		print tempuratureValue["value"]

def readLatestSoilData(amount = 0):
	soilReadings = db.child("sensor").child("soil").limit_to_first(amount).get()

	for soilReading in soilReadings.each():
		soilValue = soilReading.val()
		print soilValue["value"]


readPhotocellDataFromDateRange(0, 0, 0, 1)
# functions to push that motor operation has completed



