from flask import render_template, redirect, url_for, request
from . import core_bp

@core_bp.route('/')
def land_page():
    message = "This is a landing page"
    return render_template(template_name_or_list='landing_page.html', message=message)

