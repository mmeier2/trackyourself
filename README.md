trackyourself
=============

CSE360 Health management website 

Dependencies:
This web app requires the following in order to properly execute:
	Python 2.7+ (Not Python 3+): https://www.python.org/download/releases/2.7.2
	Django 1.6.2: https://www.djangoproject.com/download/
	MySQL: http://dev.mysql.com/downloads/
	MySQL Python Connector: http://dev.mysql.com/downloads/connector/python/

Set up:
	1. Navigate to settings.py, change the TEMPLATE_DIRS (line 86) and the STATICFILES_DIRS (line 111) strings to '*location of the project*/templates' and  '*location of the project*/static'respectively. (To find the location of the project, navigate the the project in terminal and enter the commmand pwd).
	2. Run the SQL script in "SE_DB_Scripts.txt" in mySQL Workbench  

How to run:
	1. Open up a terminal session
	2. Navigate to the project, the base directory trackyouself
	3. Run the command: python manage.py runserver
	(ex output): 0 errors found
				April 24, 2014 - 20:25:14
				Django version 1.6.2, using settings 'track_yourself.settings'
				Starting development server at http://127.0.0.1:8000/
				Quit the server with CONTROL-C.
	4. Open up a browser and paste the development server (ex. http://127.0.0.1:8000/) as a url

