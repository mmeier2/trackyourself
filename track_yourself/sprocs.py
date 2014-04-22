import mysql.connector

DB_NAME = 'SE_Database_Schema'

class user_table():
    @staticmethod
    def get_user(email, password):
        fname = lname = email_id = user_ID = None
        cnx = mysql.connector.connect(user='root', database=DB_NAME)
        cursor = cnx.cursor()
        get_user = ("SELECT userId, firstName, lastName, emailId FROM User WHERE emailid=%s AND password=%s")
        user_cred = (email, password)
        try:
            cursor.execute(get_user, user_cred)
            for (userId, firstName, lastName, emailId) in cursor:
                    fname = firstName
                    lname = lastName
                    email_id = emailId
                    user_ID = userId
            cursor.close()
            cnx.close()
        except mysql.connector.Error as err:
            pass
        return {'user_ID':user_ID, 'fname':fname, 'lname':lname, 'email_id':email_id}

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

    @staticmethod
    def add_data(data_data):
        add_data = ("INSERT INTO Data (date, userId, duration, descriptionType, dataType) VALUES (%s, %s, %s, %s, %s)")
        cnx = mysql.connector.connect(user='root', database=DB_NAME)
        cursor = cnx.cursor()
        try:
            cursor.execute(add_data, data_data)
            cnx.commit()
            cursor.close()
            cnx.close()
            return True
        except mysql.connector.Error as err:
            return False

class data_table():
    @staticmethod
    def get_data_summary_between(start, end, user_ID):
        dates = descriptions = durations = []
        cnx = mysql.connector.connect(user='root', database=DB_NAME)
        cursor = cnx.cursor()
        get_data = ("SELECT date, duration, descriptionType FROM Data WHERE date >= %s AND date <= %s AND dataType=1 AND userId=%s")
        interval = (start, end, user_ID)
        try:
            print get_data, interval
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