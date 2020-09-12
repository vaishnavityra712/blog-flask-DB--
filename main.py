from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
from datetime import datetime
import json
from flask_mail import Mail


with open('config.json', 'r') as c:
    params = json.load(c) ["params"]

local_server = True

app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params["gmail-user"],
    MAIL_PASSWORD = params["gmail-password"],

)

Mail = Mail(app)
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params["local_url"]
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["prod_url"]
db = SQLAlchemy(app)



class Contacts(db.Model):
    '''
    SNo, name, email, phone_num, mes, date
    '''
    SNo = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)


class Posts(db.Model):
    SNo = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(25), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    subheading = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    



@app.route('/')
def home():
    return render_template('index.html', params=params, post=post)

@app.route('/about')
def about():
    return render_template('about.html', params=params)

@app.route('/post/<string:post_slug>', methods=['GET'])
def post(post_slug):
    posts = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post)





@app.route('/contact',methods=["GET","POST"])
def contact():
    if(request.method=="POST"):
        name = request.form.get('name')
        email = request.form.get('email')
        phone_num = request.form.get('Phone Number')
        message = request.form.get('message')
        entry = Contacts(name=name, email=email, date=datetime.now(),phone_num= phone_num, message= message)
        db.session.add(entry)
        db.session.commit()
        Mail.send_message('New Message from ' + name,
                          sender=email, 
                          recipients=[params['gmail-user']],
                          body = message + "\n" + phone_num)
    

    return render_template('contact.html', params=params)



app.run(debug=True)