from flask import Flask, render_template, url_for, request
from markupsafe import escape
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY = 'dev'
)

# Filters
@app.add_template_filter
def today(date):
    return date.strftime('%d / %m / %Y ')
# Otra forma de crear decorador
# @app.add_template_filter(today, 'today')

# Funcion personalizada
@app.add_template_global
def repeat(s, n):
    return s * n

@app.route('/')
def index():
    print(url_for('index'))
    print(url_for('hello'))
    print(url_for('code', code = 'print("Hello")'))
    name = 'Franco'
    friends = ['Bruce', 'Jenni', 'Andres', 'Perla']
    date = datetime.now()
    return render_template(
        'index.html', 
        name = name, 
        friends = friends,
        date = date)

# string
# int
# float
# path
# uuid
@app.route('/hello')
@app.route('/hello/<string:name>')
@app.route('/hello/<string:name>/<int:age>/<string:email>')
def hello(name = None, age = None, email = None):
    my_data = {
        'name': name,
        'age': age,
        'email': email
    }
    
    return render_template('hello.html', data = my_data)
    # if name == None and age == None:
    #     message = 'Hello World'
    #     return render_template('hello.html', message = message)
    # elif age == None:
    #     return render_template('hello.html', name = name)
    # return render_template('hello.html', name = name, age = age)

@app.route('/code/<path:code>')
def code(code):
    return f'<code>{escape(code)}</code>'

class RegisterForm(FlaskForm):
    username = StringField('Username: ', validators = [DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password: ', validators = [DataRequired(), Length(min=6, max=40)])
    submit = SubmitField('Register: ')

@app.route('/auth/register-user', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        return f'username: {username} - password: {password}'
        
    # if request.method == 'POST':
    #     username = request.form['username']
    #     password = request.form['password']
        
    #     if len(username) >= 4 and len(username) <= 25 and len(password) >= 6 and len(password) <= 40:
    #         return f'username: {username} - password: {password}'
    #     else:
    #         error = 'Name must be between 4 and 25 characters and password must be between 6 and 40 characters'
    #         return render_template('auth/register.html', form = form, error = error)
        
    return render_template('auth/register.html', form = form)