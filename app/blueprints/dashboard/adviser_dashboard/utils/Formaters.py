from ..services.adviser_dashboard_services import AdviserDashboardServices
from ..repositories.adv_dashboard_repository import AdviserDashboardRepository

class Formaters:
    #formats the data to be put in the client side
    #Flow= repo:returns timesheet of student -> services:return compute total hours -> student target hour - total hour -> services:compute and convert to days
    @staticmethod
    def format_to_dict(ojt_list) -> list:
        result = []
        for ojt in ojt_list:
            student_timesheet = AdviserDashboardRepository.get_student_timesheet(ojt[0])
            total_hours = AdviserDashboardServices.compute_total_hours(student_timesheet)
            student_hours = ojt[4] #total hours to be completed by the student
            remaining_hours = student_hours - total_hours #decreases the total hours worked to student's total hours
            remaining_days = AdviserDashboardServices.compute_remaining_days(remaining_hours)
            data = { 
                'student_id' : ojt[0],
                'student_name': ojt[1],
                'company' : ojt[3],
                'email' : ojt[2],
                'remaining_hours': remaining_hours,
                'remaining_days': f'{remaining_days} Day/s'

            }
            result.append(data)

        return result

    #for search bar data
    @staticmethod
    def sanitize_search_data(search_data:str):
        data = search_data.strip(' ')
        data = data.split(' ')

        result = []
        for word in data:
            result.append(word.upper())

        data = " ".join(result)
        return f"%{data}%"