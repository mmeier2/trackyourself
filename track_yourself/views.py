import csv
import mysql.connector
from django.shortcuts import render
from django.shortcuts import redirect
import time
from django.http import HttpResponse
from django.template import Template
from sprocs import user_table, data_table

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
    s_time = str(request.POST.get('Syear')) + '-'
    s_time = s_time + str(request.POST.get('Smonth')) + '-'
    s_time = s_time + str(request.POST.get('Sday')) + " 00:00:00" 
    e_time = str(request.POST.get('Eyear')) + '-'
    e_time = e_time + str(request.POST.get('Emonth')) + '-'
    e_time = e_time + str(request.POST.get('Eday')) + " 23:59:59"
    user_ID = request.session['member_id']
    print s_time, e_time
    phys_data = data_table.get_data_summary_between(s_time, e_time, user_ID)
    dates = phys_data[0]
    durations = phys_data[1]
    descriptions = phys_data[2]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="file.csv"'
    writer = csv.writer(response)
    writer.writerow(["Date", "Data Type", "Measurement"])
    for (date, duration, description) in zip(dates, durations, descriptions):
        if description == '0':
            description = "Heartrate"
        elif description == '1':
            description = "Fat Percentage"
        else:
            description = "Weight"
        writer.writerow([date, description, duration])
    return response
