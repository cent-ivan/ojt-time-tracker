from datetime import datetime
import pytz
from ..repositories.student_dashboard_repository import StudentDashboardRepository

class TimeInOutService:
    @staticmethod
    def display_timestamp(id, press_type, date, timein):
        #for getting timed in or out timestamp when user loaded first time the app
        if press_type == 'True':
            if timein.hour > 12:
                return f'Timed in at {date}, {timein.hour - 12}:{timein.minute}:{timein.second} PM' #SELECT date, time_in FROM timesheettbl;
            elif timein.hour == 12:
                return f'Timed in at {date}, {timein} PM' #SELECT date, time_in FROM timesheettbl;
            else:
                return f'Timed in at {date}, {timein} AM' #SELECT date, time_in FROM timesheettbl;
        else:
            return 'Timed out'

    @staticmethod
    def get_time() -> dict:
        manila_tz = pytz.timezone('Asia/Manila')
        time = datetime.now(manila_tz)
        client_time = time.strftime(f'%H:%M %p')
        server_time = time.strftime('%H:%M:%S') #for database
        return {'client': client_time, 'server':server_time}
    
    @staticmethod
    def get_date():
        time = datetime.now()
        date = time.strftime('%Y-%m-%d')
        return datetime.strptime(date, '%Y-%m-%d').date()
    
    @staticmethod
    def compute_total_hours(timein:datetime, timeout, status):
        if status == 'Double':
            ti = timein.hour #gets the time in the database
            to = datetime.strptime(timeout, '%H:%M:%S').hour #cinverts strftime to datetime obbject
            hours_worked = None

            if ti > 12:
                hours_worked = ((to - ti)) * 2

            if to > 12: #decrease with 1 hr lunchbreak
                hours_worked = ((to - ti) - 1) * 2
            else:
                hours_worked = ((to - ti)) * 2
            return hours_worked
        else:
            ti = timein.hour #gets the time in the database
            to = datetime.strptime(timeout, '%H:%M:%S').hour #cinverts strftime to datetime obbject
            hours_worked = None
            #no decrease of 1 hour 
            if ti > 12:
                hours_worked = ((to - ti)) * 2

            if to > 12: #decrease with 1 hr lunchbreak
                hours_worked = ((to - ti) - 1)
            else:
                hours_worked = ((to - ti)) 
            return hours_worked
        
    #method for the oveall total wars
    @staticmethod
    def compute_overall_total_hours(timesheet:list) -> int:
        total = 0
        for time in timesheet:
            total += time['hours_worked']

        return total