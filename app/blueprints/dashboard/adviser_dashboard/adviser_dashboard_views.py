from flask import render_template,redirect,url_for, request, make_response
from flask_login import login_required, current_user

from . import adviser_dashboard_bp
from .repositories.adv_dashboard_repository import AdviserDashboardRepository
from ..student_dashboard.repositories.student_dashboard_repository import StudentDashboardRepository
from.services.adviser_dashboard_services import AdviserDashboardServices
from .utils.Formaters import Formaters


@adviser_dashboard_bp.route('/', methods=['POST', 'GET'])
@login_required
def index():
    if request.method == 'GET':
        try:
            id = current_user.adviserId
            name = current_user.adviserName
            school = current_user.schoolName
            #Tries if there is a search query
            search_data = request.args.get('search')
            
            if search_data == "":
                ojt_list = AdviserDashboardRepository.get_ojt_list(school)
                formated_list = Formaters.format_to_dict(ojt_list)
            else:
                #if there is a search data formats it first then searches
                search = Formaters.sanitize_search_data(search_data)
                ojt_list = AdviserDashboardRepository.get_ojt_list_filter(school, search)
                formated_list = Formaters.format_to_dict(ojt_list)
            
            return render_template('adviser_dashboard.html', uid=id, name=name, school=school, ojt_list=formated_list)
        except:
            ojt_list = AdviserDashboardRepository.get_ojt_list(school)
            formated_list = Formaters.format_to_dict(ojt_list)

            return render_template('adviser_dashboard.html', uid=id, name=name, school=school, ojt_list=formated_list)
        
    else:
        search_data = request.form.get('search')
        if search_data == "":
            return redirect(url_for('adviser_home.index'))
        else:
            #adds search to search bar
            search_data = Formaters.sanitize_search_data(search_data)
            return redirect(url_for('adviser_home.index', search = search_data))


@adviser_dashboard_bp.route('/student/<string:uid>')
@login_required
def view_student(uid):
    uid = uid
    school = current_user.schoolName
    data = AdviserDashboardRepository.get_student_data(uid)
    days_count = StudentDashboardRepository.get_count_days(uid)
    
    timesheet = AdviserDashboardRepository.get_student_timesheet(uid)
    total_hours = AdviserDashboardServices.compute_total_hours(timesheet)
    return render_template('view_student.html', uid=uid, school=school, data=data, timesheet=timesheet, days_count=days_count, total_hours=total_hours)



@adviser_dashboard_bp.app_template_filter('format_capitalize')
def format_capitalize(word) -> str:
    data = word.strip(' ')
    data = data.split(' ')

    result = []
    for word in data:
        result.append(word.capitalize())

    data = " ".join(result)
    return data