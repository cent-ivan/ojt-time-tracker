#Centralized file for the models in all of the blueprints
from .auth.models import AdviserModel, SchoolsModel, StudentModel, OjtListModel
from .dashboard.student_dashboard.models import TimeSheetModel

__all__ = [
    'AdviserModel',
    'SchoolsModel',
    'StudentModel',
    'OjtListModel'
]

all_models = [
    AdviserModel,
    SchoolsModel,
    StudentModel,
    OjtListModel,
    TimeSheetModel
]