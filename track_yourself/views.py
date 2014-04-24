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

DB_NAME = 'SE_Database_Schema'

def home(request):
    if 'member_id' in request.session:
        return render(request, 'user_home.html')
    else:
        return render(request, 'bare.html')

def Login(request):
    return render(request, 'Login.html')

def invalid_login(request):
    return render(request, "invalid_login.html")

def user_home(request):
    if 'member_id' in request.session:
        return render(request, 'user_home.html')
    else:
        return render(request, 'bare.html')

def logout(request):
    if 'member_id' in request.session:
        del request.session['member_id']
    return redirect('/')

def login_auth(request):
    user_cred = {}
    if request.POST:
        email = request.POST.get('userN')
        password = request.POST.get('userP')
        user_cred = user_table.get_user(email, password)
        if user_cred['fname'] is not None:
            request.session['member_id'] = user_cred['user_ID']
            return redirect('/user_home/')
        else:
            return redirect('/invalid_login/')

def register_auth(request):
    if request.POST:
        email = request.POST.get('userN')
        password = request.POST.get('userP')
        fname = request.POST.get('userFN')
        lname = request.POST.get('userLN')

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

def add_data(request):
    if request.POST:
        add_data = ("INSERT INTO Data (date, userId, duration, descriptionType, dataType) VALUES (%s, %s, %s, %s, %s)")
        current_time = str(time.strftime("%Y-%m-%d") + " " + time.strftime("%H:%M:%S"))
        userID = str(request.session['member_id'])
        duration = str(request.POST["duration"])
        descriptionType = str(request.POST["type"])
        dataType = str(request.POST["data_type"])
        print "entering AddWorkout() User id: 12"
        print "entering WorkoutData() user made constructor"
        print "entering Date_Obj() user made constructor"
        print "success exiting Date_Obj()"
        print "success exiting WorkoutData()"
        print "success exiting AddWorkout()"
        data_data = (current_time, userID, duration, descriptionType, dataType)
        data_was_added = user_table.add_data(data_data)
        if data_was_added:
            return redirect('/')
        else:
            return HttpResponse(status=500)

def register(request):
    return render(request, 'register.html')

def log_phys_data(request):
    if 'member_id' in request.session:
        return render(request, 'log_phys_data.html')
    else:
        return redirect('/')

def log_workout(request):
    if 'member_id' in request.session:
       return render(request, 'log_workout.html')
    else:
        return redirect('/')

def view_summary(request):
    if 'member_id' in request.session:
       return render(request, 'view_summary.html')
    else:
        return redirect('/')

def access_denied(request):
    if 'member_id' in request.session:
       return render('access_denied.html')
    else:
        return redirect('/')

def view_data_summary(request):
    if( str(request.POST.get('phys')) == 'on'):
        return view_phys_summary(request)
    elif( str(request.POST.get('workout')) == 'on'):
        return view_workout_summary(request)

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

    return render_to_response('summary.html', {'dates': dates , 'durations' : durations , 'descriptions' : descriptions , 'type' : 'Phys', 'postData' : {"s_time": start, "e_time" : end}})

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

    return render_to_response('summary.html', {'dates': dates , 'durations' : durations , 'descriptions' : descriptions , 'type' : 'Workout', 'postData' : {"s_time": start, "e_time" : end}})



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
