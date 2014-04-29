import csv
import mysql.connector
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect
import time
from django.http import HttpResponse
from django.template import Template
from sprocs import user_table, data_table
from django.views.decorators.csrf import csrf_exempt
from classes import Data, PhysData, WorkoutData, User, Month, Date_Obj

# set the database name for connection
DB_NAME = 'SE_Database_Schema'

# keep track of the user that is currently using the system
current_user = User('','','','',[],[])

# route a user depending on whether or not they are logged in
def home(request):
    if 'member_id' in request.session:
        return render(request, 'user_home.html')
    else:
        current_user.setFirstName('')
        current_user.setLastName('')
        return render(request, 'bare.html')

def Login(request):
    return render(request, 'Login.html')

# If the login credentials are invalid, send the user to invalid login page
def invalid_login(request):
    return render(request, "invalid_login.html")

# Route logged in user to logged in home page
def user_home(request):
    if 'member_id' in request.session:
        return render(request, 'user_home.html')
    else:
        return render(request, 'bare.html')

# Clear user credentials upon logout
def logout(request):
    if 'member_id' in request.session:
        del request.session['member_id']
        current_user.setFirstName('')
        current_user.setLastName('')
        current_user.setEmail('')
    return redirect('/')

# Query the database for users credentials and route them accordingly
def login_auth(request):
    user_cred = {}
    if request.POST:
        email = request.POST.get('userN')
        password = request.POST.get('userP')
        user_cred = user_table.get_user(email, password)
        if user_cred['fname'] is not None:
            request.session['member_id'] = user_cred['user_ID']
            current_user.setEmail(email)
            return redirect('/user_home/')
        else:
            return redirect('/invalid_login/')

# Enter users credintials into database and keep their credentials
def register_auth(request):
    if request.POST:
        email = request.POST.get('userN')
        password = request.POST.get('userP')
        fname = request.POST.get('userFN')
        lname = request.POST.get('userLN')
        current_user.setEmail(email)
        current_user.setFirstName(fname)
        current_user.setLastName(lname)

        # Add the user
        # Returns a boolean regarding whether the add was succesful or not
        user_data = (fname, lname, email, password)
        user_was_added = user_table.add_user(user_data)
        #Get the users credentials (needed to set session cookie)
        user_cred = user_table.get_user(email, password)
        if user_was_added:
            request.session['member_id'] = user_cred['user_ID']
            return redirect('/user_home/')
    else:
        return redirect('home')

# Insert user data into the database and append it to the current user object
def add_data(request):
    if request.POST:
        add_data = ("INSERT INTO Data (date, userId, duration, descriptionType, dataType) VALUES (%s, %s, %s, %s, %s)")
        current_time = str(time.strftime("%Y-%m-%d") + " " + time.strftime("%H:%M:%S"))
        userID = str(request.session['member_id'])
        duration = str(request.POST["duration"])
        descriptionType = str(request.POST["type"])
        dataType = str(request.POST["data_type"])
        data_data = (current_time, userID, duration, descriptionType, dataType)
        data_was_added = user_table.add_data(data_data)
        if data_was_added:
            return redirect('/')
        else:
            return HttpResponse(status=500)

# route user to register page
def register(request):
    return render(request, 'register.html')

# If a user is logged in, send them to the log phys data page
def log_phys_data(request):
    if 'member_id' in request.session:
        return render(request, 'log_phys_data.html')
    else:
        return redirect('/')

# If a user is logged in, route them to the log a workout page
def log_workout(request):
    if 'member_id' in request.session:
       return render(request, 'log_workout.html')
    else:
        return redirect('/')

# If a user is logged in, send them to the view summary page
def view_summary(request):
    if 'member_id' in request.session:
       return render(request, 'view_summary.html')
    else:
        return redirect('/')

# If a user's credentials entered upon login are not vaid, send them
# to the access denied page
def access_denied(request):
    if 'member_id' in request.session:
       return render('access_denied.html')
    else:
        return redirect('/')

# Depending on the dype of summary the user wants to see, send them to the appropriate router
def view_data_summary(request):
    if( str(request.POST.get('phys')) == 'on'):
        return view_phys_summary(request)
    elif( str(request.POST.get('workout')) == 'on'):
        return view_workout_summary(request)

# Query the database for the data requested by the user for physical data
def view_phys_summary(request):
    s_time = str(request.POST.get('Syear')) + '-'
    s_time = s_time + str(request.POST.get('Smonth')) + '-'
    s_time = s_time + str(request.POST.get('Sday')) + " 00:00:00" 
    e_time = str(request.POST.get('Eyear')) + '-'
    e_time = e_time + str(request.POST.get('Emonth')) + '-'
    e_time = e_time + str(request.POST.get('Eday')) + " 23:59:59"
    user_ID = request.session['member_id'] 
    phys_data = data_table.get_data_summary_between(s_time, e_time, 1, user_ID)
    dates = phys_data[0]
    durations = phys_data[1]
    descriptions = phys_data[2]
    start = str(request.POST.get('Smonth')) + '/' + str(request.POST.get('Sday')) + '/' + str(request.POST.get('Syear'))
    end = str(request.POST.get('Emonth')) + '/' + str(request.POST.get('Eday')) + '/' + str(request.POST.get('Eyear'))
    
    print dates

    return render_to_response('summary.html', {'dates': dates , 'durations' : durations , 'descriptions' : descriptions , 'type' : 'Phys', 'postData' : {"s_time": start, "e_time" : end, "sTime" : s_time, "eTime" : e_time}})

def view_workout_summary(request):
    s_time = str(request.POST.get('Syear')) + '-'
    s_time = s_time + str(request.POST.get('Smonth')) + '-'
    s_time = s_time + str(request.POST.get('Sday')) + " 00:00:00" 
    e_time = str(request.POST.get('Eyear')) + '-'
    e_time = e_time + str(request.POST.get('Emonth')) + '-'
    e_time = e_time + str(request.POST.get('Eday')) + " 23:59:59"
    user_ID = request.session['member_id'] 
    phys_data = data_table.get_data_summary_between(s_time, e_time, 0, user_ID)
    dates = phys_data[0]
    durations = phys_data[1]
    descriptions = phys_data[2]
    start = str(request.POST.get('Smonth')) + '/' + str(request.POST.get('Sday')) + '/' + str(request.POST.get('Syear'))
    end = str(request.POST.get('Emonth')) + '/' + str(request.POST.get('Eday')) + '/' + str(request.POST.get('Eyear'))
    print dates

    return render_to_response('summary.html', {'dates': dates , 'durations' : durations , 'descriptions' : descriptions , 'type' : 'Workout', 'postData' : {"s_time": start, "e_time" : end, "sTime" : s_time, "eTime" : e_time}})

# This funciton creates a csv out of the data in the summary being viewed by the user
@csrf_exempt
def create_csv(request):  
    if request.POST:
        Phys = ["Heartrate", "Fat Percentage", "Weight"]
        Work = ["Running", "Weight Lifting", "Swimming"]
        dates = []
        durations = []
        descriptions = []
        user_ID = request.session['member_id'] 
        s_time = request.POST['s_time']
        e_time = request.POST['e_time']
        if request.POST['type'] == "Workout":
            data_type = 0
        else:
            data_type = 1
        phys_data = data_table.get_data_summary_between(s_time, e_time, data_type, user_ID)
        dates = phys_data[0]
        durations = phys_data[1]
        descriptions = phys_data[2]  
        print phys_data
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="summary.csv"'
        writer = csv.writer(response)
        writer.writerow(["Date", "Data Type", "Measurement"])
        for (date, duration, description) in zip(dates, durations, descriptions):
            if data_type == 0:
                description = Work[int(description)]
            else:
                description = Phys[int(description)]
            writer.writerow([date, description, duration]) 
        return response
