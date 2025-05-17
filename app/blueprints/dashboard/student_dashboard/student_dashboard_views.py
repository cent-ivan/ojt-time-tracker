from datetime import datetime, timedelta, timezone, time
from flask import render_template,redirect,url_for, request, make_response
from flask_login import login_required, current_user

from . import stud_dashboard_bp
from .services.timeinout_service import TimeInOutService
from .repositories.student_dashboard_repository import StudentDashboardRepository

@stud_dashboard_bp.route('/', methods=['POST', 'GET'])
@login_required
def index():
    if request.method == 'GET':
        uid = current_user.studentId
        name = current_user.studentName
        student_total_hours = current_user.totalHours
        days_count = StudentDashboardRepository.get_count_days(current_user.studentId)
        current_date = TimeInOutService.get_date()

        time_client_display = {
            'date': current_date,
            'day': datetime.now().strftime('%a'),
            'am_pm': datetime.now().strftime('%p')
        }
        
        #Change that if the user clicked it, it changes from Time In to Time Out
        #checks first if there is a cookie if not creates a cookie
        try:
            #sets cookie to expire in 20 hours
            time_expiration = datetime.now(timezone.utc) + timedelta(hours=20)
            is_pressed_cookie = request.cookies['time_pressed']


            timesheet = StudentDashboardRepository.get_timesheet(current_user.studentId) #all timesheet
            total_hours = TimeInOutService.compute_overall_total_hours(timesheet)

            if StudentDashboardRepository.get_timein(current_user.studentId, current_date) == None:
                return render_template('student_dashboard.html', 
                                    uid = uid,
                                    time_client_display = time_client_display,
                                    name=name, 
                                    student_hours=student_total_hours,
                                    days_count = days_count,
                                    total_hours = total_hours,
                                    timesheet = timesheet,
                                    time=f"", 
                                    is_pressed=is_pressed_cookie, 
                                    is_showed = 'True'
                                    )

            else:
                timein = StudentDashboardRepository.get_timein(current_user.studentId, current_date)[0] 
                timestamp = TimeInOutService.display_timestamp(current_user.studentId, is_pressed_cookie, current_date, timein) #get the timestamp to display underneath the button
                return render_template('student_dashboard.html', 
                                    uid = uid,
                                    time_client_display = time_client_display,
                                    name=name, 
                                    student_hours=student_total_hours,
                                    days_count = days_count,
                                    total_hours = total_hours,
                                    timesheet = timesheet,
                                    time=timestamp, 
                                    is_pressed=is_pressed_cookie, 
                                    is_showed = 'True'
                                    )
        
            
        except KeyError:
            #If cookie do not exist it will make it
            #sets cookie to expire in 20 hours
            timesheet = StudentDashboardRepository.get_timesheet(current_user.studentId)
            total_hours = TimeInOutService.compute_overall_total_hours(timesheet)
            time_expiration = datetime.now(timezone.utc) + timedelta(hours=20)
            response = make_response( render_template('student_dashboard.html', 
                                                      uid = uid,
                                                      time_client_display = time_client_display,
                                                      name=name, 
                                                      student_hours=student_total_hours,
                                                      days_count = days_count,
                                                      total_hours = total_hours,
                                                      timesheet = timesheet,
                                                      time=f"", 
                                                      is_pressed='False', 
                                                      is_showed = 'False')
                                                )
            response.set_cookie(
                key='time_pressed',
                value='False',
                expires = time_expiration
            )
            return response
        
        # except:
        #     return "An Uknown Error"

    else:
        #POST
        time_service = TimeInOutService()
        current_date  = time_service.get_date() #returns current time when clicked, time for client and server to store
        time_pressed = time_service.get_time()
        
        #sets cookie to expire in 20 hours
        time_expiration = datetime.now(timezone.utc) + timedelta(hours=20)

        is_pressed = 'True'
        is_pressed_cookie = request.cookies['time_pressed']

        if is_pressed_cookie == is_pressed: 
            status = request.form.get('status')
            note = request.form.get('note')

            #compute for the total hours worked. (Get time in time in db -> compute total hours work -> insert to db)
            timein = StudentDashboardRepository.get_timein(current_user.studentId, current_date)[0] 
            hours_worked = TimeInOutService.compute_total_hours(timein, time_pressed['server'],status) if TimeInOutService.compute_total_hours(timein, time_pressed['server'],status) != 0 else 0
            StudentDashboardRepository.insert_timeout(current_user.studentId, current_date, time_pressed['server'], hours_worked ,status, note)

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
            #inserts time in the database
            StudentDashboardRepository.insert_timein(current_user.studentId, current_date, time_pressed['server'])

            #if the user clicked time out it displays 'Time In', then it will change it to Time Out if pressed hence True == Pressed
            response = make_response(redirect(url_for('student_home.index')))
            response.set_cookie(
                key='time_pressed',
                value=is_pressed,
                expires = time_expiration
            )
            return response
        
@stud_dashboard_bp.app_template_filter('format_times')
def format_time(input_time) -> str:
    try:
        if isinstance(input_time, (datetime, time)):
            hour = input_time.hour
            minute = f"{input_time.minute}"

        elif isinstance(input_time, int):
            if input_time == 0:
                return "No Time"


        # Convert to 12-hour format
        if hour == 0:
            return f"12:{minute} AM"
        elif hour < 12:
            return f"{hour}:{minute} AM"
        elif hour == 12:
            return f"{hour}:{minute} PM"
        else:
            return f"{hour - 12}:{minute} PM"
    
    except Exception as e:
        return "Invalid time"