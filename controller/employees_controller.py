from flask import Blueprint, render_template
from flask_login import login_required

employees = Blueprint('employees', __name__)


@employees.route('/employees/current')
@login_required
def get_employee():
    return render_template('employee.html')
