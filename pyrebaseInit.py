import pyrebase
import datetime
import json
from time import gmtime, strftime

class Pyrebase:
	db = ''

	def __init__(self, apiKey, authDomain, databaseURL, storageBucket):
		config = {
			"apiKey" : apiKey,
			"authDomain" : authDomain,
			"databaseURL" : databaseURL,
			"storageBucket" : storageBucket
		}
		firebase = pyrebase.initialize_app(config)
		self.db = firebase.database()

	# Used to convert datetime object into UTC date format
	def convertDatetimeToUTC(self, dateTime):
		UTCDateTime = (dateTime - datetime.datetime(1970, 1, 1)).total_seconds()
		return UTCDateTime

	# writes to firebase table sensor/photocell with the current date and inputted value
	def writeToPhotocellTable(self, value):
		data = {
			"value" : value,
			"datetime" : convertDatetimeToUTC(datetime.datetime.now())
		}
		self.db.child("sensor").child("photocell").push(data)

	# writes to firebase table sensor/humidity with the current date and inputted value
	def writeToHumidityTable(self, value):
		data = {
			"value" : value,
			"datetime" : convertDatetimeToUTC(datetime.datetime.now())
		}
		self.db.child("sensor").child("humidity").push(data)

	# writes to firebase table sensor/tempurature with the current date and inputted value
	def writeToTempuratureTable(self, value):
		data = {
			"value" : value,
			"datetime" : convertDatetimeToUTC(datetime.datetime.now())
		}
		self.db.child("sensor").child("tempurature").push(data)

	# writes to firebase table sensor/soil with the current date and inputted value
	def writeToSoilTable(self, value):
		data = {
			"value" : value,
			"datetime" : convertDatetimeToUTC(datetime.datetime.now())
		}
		self.db.child("sensor").child("soil").push(data)

	# writes to firebase table 'motor/fan' sets value to 1 and datetime to now
	def logFanOn(self):
		data = {
			"value" : 1,
			"datetime" : self.convertDatetimeToUTC(datetime.datetime.now())
		}
		self.db.child("motor").child("fan").push(data)

	# writes to firebase table 'motor/fan' sets value to 0 and datetime to now
	def logFanOff(self):
		data = {
			"value" : 0,
			"datetime" : self.convertDatetimeToUTC(datetime.datetime.now())
		}
		self.db.child("motor").child("fan").push(data)

	# writes to firebase table 'motor/solenoid' sets value to 1 and datetime to now
	def logSolenoidOn(self):
		data = {
			"value" : 1,
			"datetime" : self.convertDatetimeToUTC(datetime.datetime.now())
		}
		self.db.child("motor").child("solenoid").push(data)

	# writes to firebase table 'motor/solenoid' sets value to 0 and datetime to now
	def logSolenoidOff(self):
		data = {
			"value" : 0,
			"datetime" : self.convertDatetimeToUTC(datetime.datetime.now())
		}
		self.db.child("motor").child("solenoid").push(data)

	def logWaterTankIsFull(self):
		data = {
			"value" : 1,
			"datetime" : self.convertDatetimeToUTC(datetime.datetime.now())
		}
		self.db.child("sensor").child("float").push(data)

	def logWaterTankNotFull(self):
		data = {
			"value" : 0,
			"datetime" : self.convertDatetimeToUTC(datetime.datetime.now())
		}
		self.db.child("sensor").child("float").push(data)

	# TODO save all reading values into array

	def readPhotocellDataFromDateRange(self, seconds = 0, minutes = 0, hours = 0, days = 0):
		endDateRange = datetime.datetime.now()
		startDateRange = endDateRange - datetime.timedelta(seconds=seconds) - datetime.timedelta(minutes=minutes) - datetime.timedelta(hours=hours) - datetime.timedelta(days=days)
		
		photocellReadings = self.db.child("sensor").child("photocell").order_by_child("datetime").start_at(convertDatetimeToUTC(startDateRange)).end_at(convertDatetimeToUTC(endDateRange)).get()

		for photocellReading in photocellReadings.each():
			photocellValue = photocellReading.val()
			print photocellValue["value"]

	def readHumidityDataFromDateRange(self, seconds = 0, minutes = 0, hours = 0, days = 0):
		endDateRange = datetime.datetime.now()
		startDateRange = endDateRange - datetime.timedelta(seconds=seconds) - datetime.timedelta(minutes=minutes) - datetime.timedelta(hours=hours) - datetime.timedelta(days=days)
		
		humidityReadings = self.db.child("sensor").child("humidity").order_by_child("datetime").start_at(startDateRange).end_at(endDateRange).get()

		for humidityReading in humidityReadings.each():
			humidityValue = humidityReading.val()
			print humidityValue["value"]

	def readTempuratureDataFromDateRange(self, seconds = 0, minutes = 0, hours = 0, days = 0):
		endDateRange = datetime.datetime.now()
		startDateRange = endDateRange - datetime.timedelta(seconds=seconds) - datetime.timedelta(minutes=minutes) - datetime.timedelta(hours=hours) - datetime.timedelta(days=days)
		
		tempuratureReadings = self.db.child("sensor").child("tempurature").order_by_child("datetime").start_at(startDateRange).end_at(endDateRange).get()

		for tempuratureReading in tempuratureReadings.each():
			tempuratureValue = tempuratureReading.val()
			print tempuratureValue["value"]

	def readSoilDataFromDateRange(self, seconds = 0, minutes = 0, hours = 0, days = 0):
		endDateRange = datetime.datetime.now()
		startDateRange = endDateRange - datetime.timedelta(seconds=seconds) - datetime.timedelta(minutes=minutes) - datetime.timedelta(hours=hours) - datetime.timedelta(days=days)
		
		soilReadings = self.db.child("sensor").child("soil").order_by_child("datetime").start_at(startDateRange).end_at(endDateRange).get()

		for soilReading in soilReadings.each():
			soilValue = soilReading.val()
			print soilValue["value"]

	# reads x amount of latest entries
	def readLatestPhotocellData(self, amount = 0):
		photocellReadings = self.db.child("sensor").child("photocell").limit_to_first(amount).get()

		for photocellReading in photocellReadings.each():
			photocellValue = photocellReading.val()
			print photocellValue["value"]

	def readLatestHumidityData(self, amount = 0):
		humidityReadings = self.db.child("sensor").child("humidity").limit_to_first(amount).get()

		for humidityReading in humidityReadings.each():
			humidityValue = humidityReading.val()
			print humidityValue["value"]

	def readLatestTempuratureData(self, amount = 0):
		tempuratureReadings = self.db.child("sensor").child("tempurature").limit_to_first(amount).get()

		for tempuratureReading in tempuratureReadings.each():
			tempuratureValue = tempuratureReading.val()
			print tempuratureValue["value"]

	def readLatestSoilData(self, amount = 0):
		soilReadings = self.db.child("sensor").child("soil").limit_to_first(amount).get()

		for soilReading in soilReadings.each():
			soilValue = soilReading.val()
			print soilValue["value"]