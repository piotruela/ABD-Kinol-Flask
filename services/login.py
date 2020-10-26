import flask

app = flask.Flask(__name__)


@app.route('/login', methods=['POST'])
def login():
    user = get_user(flask.request.form['username'])

    if user.check_password(flask.request.form['password']):
        login_user(user)
        app.logger.info('%s logged in successfully', user.username)
        return flask.redirect(flask.url_for('index'))
    else:
        app.logger.info('%s failed to log in', user.username)
        flask.abort(401)
