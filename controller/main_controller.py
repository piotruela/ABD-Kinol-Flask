from flask import Blueprint, render_template, redirect
from flask_login import login_required

main = Blueprint('main', __name__)


@main.route('/index')
@login_required
def index():
    return render_template('index.html')


@main.route('/')
@login_required
def index_blank():
    return redirect('/index')
