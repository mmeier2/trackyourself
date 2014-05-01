import mysql.connector
from classes import Data, PhysData, WorkoutData, User, Month, Date_Obj

DB_NAME = 'SE_Database_Schema'
current_user = User('','','','',[],[])

# Class of methods to interact with the user table in the databse
class user_table():
    # Stored query to get the credentials users
    @staticmethod
    def get_user(email, password):
        fname = lname = email_id = user_ID = doctor = None
        cnx = mysql.connector.connect(user='root', database=DB_NAME)
        cursor = cnx.cursor()
        get_user = ("SELECT userId, firstName, lastName, emailId, doctorFirstName FROM User WHERE emailid=%s AND password=%s")
        user_cred = (email, password)
        current_user.setEmail(email)
        try:
            cursor.execute(get_user, user_cred)
            #for (userId, firstName, lastName, emailId, doctorName) in cursor:
            for (userId, firstName, lastName, emailId, doctorName) in cursor:
                    fname = firstName
                    lname = lastName
                    email_id = emailId
                    user_ID = userId
                    if(doctorName):
                        doctor = "user_doc.html"
                    else:
                        doctor = "user_nodoc.html"
                    #doctor = "user_nodoc.html"
            cursor.close()
            cnx.close()
        except mysql.connector.Error as err:
            print err
            pass
        return {'user_ID':user_ID, 'fname':fname, 'lname':lname, 'email_id':email_id, 'doctor' : doctor}

    @staticmethod
    def get_doctor(user_data):
        d_fname = d_lname = d_email = None
        cnx = mysql.connector.connect(user='root', database=DB_NAME)
        cursor = cnx.cursor()
        get_user = ("SELECT doctorFirstName, doctorLastName, doctorEmail FROM User WHERE userId="+ str(user_data) )
        try:
            cursor.execute(get_user)
            #for (userId, firstName, lastName, emailId, doctorName) in cursor:
            for (doctorFirstName, doctorLastName, doctorEmail) in cursor:
                    d_fname = doctorFirstName
                    d_lname = doctorLastName
                    d_email = doctorEmail
            cursor.close()
            cnx.close()
        except mysql.connector.Error as err:
            print err
            pass
        return {'fname':d_fname, 'lname':d_lname, 'email':d_email}



    # Method that creates and inserts a new user into the database
    @staticmethod
    def add_user(user_data):
        add_user = ("INSERT INTO User (firstName, lastName, emailid, password) VALUES (%s, %s, %s, %s)")
        cnx = mysql.connector.connect(user='root', database=DB_NAME)
        cursor = cnx.cursor()
        try:
            cursor.execute(add_user, user_data)
            cnx.commit()
            cursor.close()
            cnx.close()
            return True
        except mysql.connector.Error as err:
            return False

    # Method that inserts new data for a user into the database
    @staticmethod
    def add_data(data_data):
        add_data = ("INSERT INTO Data (date, userId, duration, descriptionType, dataType) VALUES (%s, %s, %s, %s, %s)")
        cnx = mysql.connector.connect(user='root', database=DB_NAME)
        cursor = cnx.cursor()
        if(data_data[3]):
            current_user.addPhys(data_data[0])
        else:
            current_user.addWorkout(data_data[0])
        try:
            cursor.execute(add_data, data_data)
            cnx.commit()
            cursor.close()
            cnx.close()
            return True
        except mysql.connector.Error as err:
            return False


    @staticmethod
    def add_doctor(data_data):
        add_data = ("UPDATE User SET doctorFirstName = %s, doctorLastName = %s, doctorEmail = %s WHERE userId = %s")
        cnx = mysql.connector.connect(user='root', database=DB_NAME)
        cursor = cnx.cursor()
        print add_data
        print data_data
        try:
            cursor.execute(add_data, data_data)
            cnx.commit()
            cursor.close()
            cnx.close()
            return True
        except mysql.connector.Error as err:
            return False

# Class that provides simple methods for getting data from the data database
class data_table():
    # Method to retreive any type of data between a set time period in the data database
    @staticmethod
    def get_data_summary_between(start, end, data_type, user_ID):
        cnx = mysql.connector.connect(user='root', database=DB_NAME)
        cursor = cnx.cursor()
        get_data = ("SELECT date, duration, descriptionType FROM Data WHERE date >= %s AND date <= %s AND dataType=%s AND userId=%s")
        interval = (start, end, data_type, user_ID)
        try:
            dates = []
            durations = []
            descriptions = []
            if (data_type == '1'):
                userData = PhysData(start, end, interval)
            else:
                userData = WorkoutData(start, interval, user_ID)
            cursor.execute(get_data, interval)
            for (date, duration, descriptionType) in cursor:
                if date is not None and duration is not None and descriptionType is not None:
                    dates.append(date)
                    durations.append(duration)
                    descriptions.append(descriptionType)

            cursor.close()
            cnx.close()
        except mysql.connector.Error as err:
            print "Error trying to access data in Data table"
            print err
        return [dates, durations, descriptions]