from datetime import datetime, timedelta

from flask import Flask, jsonify, request, session

from database import Connection, User

app = Flask(__name__)
app.secret_key = "1299292929278378"
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)

@app.route('/')
def home():
    return 'home'

@app.before_request
def before_request_callback():
    if str(request.url_rule) == '/login':
        return
    sess = dict(session)
    if 'user' not in sess:
        raise Exception("Please login first")


@app.route('/login', methods=['POST'])
def login():
    req = request.json
    connection = Connection()
    res = {'cd': '888', 'sms': 'Invalid login'}
    con_status = connection.verify_user(req['username'], req['password'])
    if con_status['isValid']:
        session.permanent = True
        session['user'] = con_status['userData']
        res['cd'] = '000'
        res['sms'] = 'Valid login'
        res['session'] = session
    return jsonify(res)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return {'cd': '000', 'sms': 'Logout success!'}

@app.route('/change-password/<username>', methods=['POST'])
def change_password(username):
    req = request.json
    user = User()
    res = {'cd': '888', 'sms': 'Password was not changed'}
    if not user.set_user_by_username(username):
        res['sms'] = 'Username not found'
    if user.change_password(req['password']):
        res['cd'] = '000'
        res['sms'] = 'Password is changed'
    return jsonify(res)

@app.route('/users')
def get_all_users():
    return jsonify(User.get_all_user())

app.run(debug=True)
