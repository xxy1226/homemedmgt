from flask import Flask, render_template, request, make_response, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length, Email
import pymongo

app=Flask(__name__)
app.secret_key='forsession'

mymon=pymongo.MongoClient('localhost', 27017)
mydb=mymon['xxiablog']
mycol=mydb['users']


class RegisterForm(FlaskForm):
    username = StringField(label='用户名：', validators=[DataRequired()])
    email = StringField(label='邮箱：', validators=[DataRequired(), Email(message='邮箱格式错误')])
    password = PasswordField(label='密码：', validators=[DataRequired(), Length(6, 16, message='密码格式错误')])
    password2 = PasswordField(label='确认密码：', validators=[DataRequired(), Length(6, 16, message='密码格式错误'), EqualTo('password', message='密码不一致')])
    submit = SubmitField(label='注册')

class Member():
    def __init__(self, username, email, password):
        self.username = username
        self.email = emaila
        self.password = password

# @app.route('/home/<name>/<int:age>')
# def home(name,age):
#     return f'Welcome to home! {name} at {age}'

@app.route('/home/<name>')
def home(name):
    return render_template('index.html', name=name)

# @app.route('/', methods=['GET'])
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # username = request.args.get('username')
        # password = request.args.get('password')
        username = request.form['username']
        password = request.form['password']
        if username == "xxia" and password == "123123":
            return f"<html><body>Welcomd {username}</body></html>"
        else:
            return f"<html><body>Welcome!</body></html>"
    else:
        return render_template('index.html')


@app.route('/cookie', methods=['GET'])
def cookie():
    resp = make_response("<html><body>Cookie</body></html>")
    resp.set_cookie('name', 'xxiac')
    return resp

@app.route('/session', methods=['GET'])
def sess():
    resp = make_response("<html><body>Session.<a href='/getValue'>Get Value</a></body></html>")
    session['name'] = 'xxias'
    return resp

@app.route('/getValue')
def getValue():
    if 'name' in session:
        name=session['name']
        return render_template('getvalue.html', name=name)

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/success', methods=['POST'])
def success():
    if request.method=='POST':
        f = request.files['file']
        f.save(f.filename)
        return render_template('success.html', name=f.filename)

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['email']!='xxia@test.com' or request.form['password']!='123123':
            error='Invalid account.'
        else:
            flash('Login successfully')
            return redirect(url_for('loginsuccess'))
    return render_template('login.html', error=error)

@app.route('/loginsuccess')
def loginsuccess():
    return render_template('loginsuccess.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if request.method == 'POST':
        if register_form.validate_on_submit():
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')

            if username == 'xxia' and email == 'xxia@test.com':
                return 'Register success, username: {}, email: {}, password: {}'.format(username, email, password)
            else:
                return 'Error'
        else:
            return 'Invalid'
        
    return render_template('register.html', form=register_form)

@app.route('/mongotest', methods=['GET', 'POST'])
def mongotest():
    register_form = RegisterForm()
    if request.method == 'POST':
        if register_form.validate_on_submit():
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')

            if mycol.find_one({'username': username}):
                return '用户名已被使用'

            Member = {'username':username, 'email':email, 'password':password}
            mycol.insert_one(Member)
            return '注册成功'
        else:
            return '无效'

    return render_template('mongotest.html', form=register_form)

if __name__ == '__main__':
    app.run()
    # app.run(debug=True,host="andrewxxia.ittun.com")