from datetime import datetime, timedelta, timezone
from flask import render_template,redirect,url_for, request, make_response
from flask_login import login_required, current_user

from . import stud_dashboard_bp
from .services.timeinout_service import TimeInOutService
from .repositories.student_dashboard_repository import StudentDashboardRepository

@stud_dashboard_bp.route('/', methods=['POST', 'GET'])
@login_required
def index():
    name = current_user.studentName
    total_hours = current_user.totalHours
    
    if request.method == 'GET':
        time_service = TimeInOutService()
        
        #Change that if the user clicked it, it changes from Time In to Time Out
        #checks first if there is a cookie if not creates a cookie
        try:
            #sets cookie to expire in 20 hours
            time_expiration = datetime.now(timezone.utc) + timedelta(hours=20)
            is_pressed_cookie = request.cookies['time_pressed']

            timestamp = StudentDashboardRepository.get_timestamp(current_user.studentId, is_pressed_cookie) #get the timestamp
            return render_template('student_dashboard.html', name=name, time=timestamp, is_pressed=is_pressed_cookie, is_showed = 'True')
        
            
        except KeyError:
            #If cookie do not exist it will make it
            #sets cookie to expire in 20 hours
            time_expiration = datetime.now(timezone.utc) + timedelta(hours=20)
            response = make_response( render_template('student_dashboard.html', name=name, time=f"", is_pressed='False', is_showed = 'False'))
            response.set_cookie(
                key='time_pressed',
                value='False',
                expires = time_expiration
            )
            return response
        
        except:
            return "An Uknown Error"

    else:
        #POST
        time_service = TimeInOutService()
        time_pressed  = time_service.get_time() #returns current time when clicked, time for client and server to store
    
        #sets cookie to expire in 20 hours
        time_expiration = datetime.now(timezone.utc) + timedelta(hours=20)

        is_pressed = 'True'
        is_pressed_cookie = request.cookies['time_pressed']

        if is_pressed_cookie == is_pressed: 
            #PUT TIME OUT DATA HERE. Insert Time Out. Button turns to 'Time In'

            #if the user clicked time in it displays 'Time out', then it will change it to Time In if pressed hence False == Not Pressed
            #name=username, time=show time when pressed, is_pressed=pass a bool if botton is pressed for changing the button, is_showed=pass a bool to show the time if pressed
            response = make_response(redirect(url_for('student_home.index')))
            response.set_cookie(
                key='time_pressed',
                value='False',
                expires = time_expiration
            )
            return response
        else:
            #PUT TIME IN DATA HERE. Insert Time In. Button turns to 'Time In'


            #if the user clicked time out it displays 'Time In', then it will change it to Time Out if pressed hence True == Pressed
            response = make_response(redirect(url_for('student_home.index')))
            response.set_cookie(
                key='time_pressed',
                value=is_pressed,
                expires = time_expiration
            )
            return response