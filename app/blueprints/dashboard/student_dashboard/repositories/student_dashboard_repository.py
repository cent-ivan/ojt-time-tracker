from datetime import date, datetime

from .....extensions import db, insert, select, and_, SQLAlchemyError, IntegrityError
from ..student_dashboard_models import TimeSheetModel


class StudentDashboardRepository:
    @staticmethod
    def get_timestamp(id, press_type):
        #for getting timed in or out timestamp when user loaded first time the app
        if press_type == 'True':
            return 'Timed in at 05/13/2025, 1:44 PM' #SELECT time_in FROM timesheettbl;
        else:
            return 'Timed out at 05/13/2025, 5:00 PM' #SELECT time_out FROM timesheettbl;

    @staticmethod
    def insert_timestamp(data):
        if data['is_timein'] and data['date'] != '':
            pass