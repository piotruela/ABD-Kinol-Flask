from flask import Blueprint, render_template, redirect
from flask_login import login_required

main = Blueprint('main', __name__)


@login_required
@main.route('/index')
def index():
    return render_template('index.html')


@main.route('/')
def index_blank():
    return redirect('/index')
