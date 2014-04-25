# Parent class for the two types of data
class Data():
	def __init__(self, d_type, date):
		self.d_type = d_type
		self.date = date

	def getType(self):
		return self.d_type

	def setType(self, d_type):
		self.d_type = d_type

	def getDate(self):
		return self.date

	def setDate(self, date):
		self.date = date

# Class to hold phys data in
class PhysData(Data):

	def __init__(self, measurement, phys, date ):
		self.measurement =  measurement
		self.phys = phys
		self.date = date

	def getMeas(self):
		return self.measurement

	def setMeas(self, measurement):
		self.measurement = measurement

#Class to hold workout data in
class WorkoutData(Data):

	def __init__(self, date, duration, d_type):
		self.d_type = d_type
		self.date = date
		self.duration = duration

	def getDuration(self):
		return self.duration

	def setDuration(self, duration):
		self.duration = duration

# Object to help months
class Month():
	def __init__(self, name, value):
		self.name = name
		self.value = value

	def getName(self):
		return self.name

	def getVale(self):
		return self.value

	def setName(self, name):
		self.name = name

	def setValue(self, value):
		self.value = value

# Date object with simplifies formatting of dates
class Date_Obj():
	def __init__(self, month, day, year, week):
		self. month = month
		self.day = day
		self.year = year
		self.week = week

	def getMonth(self):
		return self.month

	def getDay(self):
		return self.day

	def getYear(self):
		return self.year

	def getWeek(self):
		return self.week

# User obj which is used to track the current users credentials and data
class User():
	def __init__(self, iD, email, firstName, lastName, workoutList, physList):
		self.id = iD
		self.email = email
		self.firstName = firstName
		self.lastName = lastName
		self.workoutList = workoutList
		self.physList = physList


	def getEmail(self):
		return self.email

	def getFirstName(self):
		return self.firstName

	def getLastName(self):
		return self.lastName

	def setEmail(self, email):
		self.email = email

	def setFistName(self, firstName):
		self.firstName = firstName

	def setLastName(self, lastName):
		self.lastName = lastName

	def addWorkout(self, workout):
		self.workoutList.append(workout)

	def addPhys(self, phys):
		self.physList.append(phys)

	def getWorkouts(self):
		return self.workoutList

	def getPhys(self):
		return self.physList
