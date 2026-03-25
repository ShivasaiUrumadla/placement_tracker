
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,render_template,request,redirect,session,url_for
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
app=Flask(__name__)
app.secret_key = "secret123"  

#CONNECTING FLASK APP TO MYSQL DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Qwerty1%40@localhost/placement'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#---------------CREATING TABLE USING PYTHON INSTEAD OF WRTING SQL MANUALLY---------------
class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(100))
    email=db.Column(db.String(100))


class University(db.Model):
    __tablename__="university"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(100))
    email=db.Column(db.String(100))
   
#-------------CREATING TABLE USING PYTHON INSTEAD OF WRTING SQL MANUALLY---------
class Task(db.Model):
    __tablename__ = 'tasks'   

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    taks_name = db.Column(db.String(255))
    status = db.Column(db.String(50))

#--------------HOME REDIRECTS TO REGISTER-------------------------
@app.route('/')
def index():
    # Force logout if the user visits the root page so it ALWAYS shows register first
    # session.pop('user', None)
    if 'user' in session:
        return redirect('/dashboard')
    return redirect('/login')   

#--------------CREATING DASHBOARD PAGE-------------------------
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    tasks = Task.query.all()
    users = User.query.all()
    return render_template('dashboard.html',user=session['user'], users=users, tasks=tasks)

# ---------------NOTIFICATIONS PAGE-------------------------
@app.route('/notifications')
def notifications():
    if 'user' not in session: return redirect('/login')
    return render_template('notifications.html', user=session['user'])

#--------------CURATED PRACTICE PAGES-------------------------
@app.route('/dsa')
def dsa():
    if 'user' not in session: return redirect('/login')
    return render_template('dsa.html', user=session['user'])

@app.route('/aptitude')
def aptitude():
    if 'user' not in session: return redirect('/login')
    return render_template('aptitude.html', user=session['user'])

@app.route('/sql')
def sql():
    if 'user' not in session: return redirect('/login')
    return render_template('sql.html', user=session['user'])

@app.route('/html')
def html_page():
    if 'user' not in session: return redirect('/login')
    return render_template('html.html', user=session['user'])

@app.route('/css')
def css_page():
    if 'user' not in session: return redirect('/login')
    return render_template('css.html', user=session['user'])

@app.route('/javascript')
def javascript():
    if 'user' not in session: return redirect('/login')
    return render_template('javascript.html', user=session['user'])

@app.route('/react')
def react():
    if 'user' not in session: return redirect('/login')
    return render_template('react.html', user=session['user'])

@app.route('/nodejs')
def nodejs():
    if 'user' not in session: return redirect('/login')
    return render_template('nodejs.html', user=session['user'])

@app.route('/express')
def express_page():
    if 'user' not in session: return redirect('/login')
    return render_template('express.html', user=session['user'])

@app.route('/flask')
def flask_page():
    if 'user' not in session: return redirect('/login')
    return render_template('flask.html', user=session['user'])

@app.route('/rest-api')
def rest_api():
    if 'user' not in session: return redirect('/login')
    return render_template('rest_api.html', user=session['user'])

@app.route('/mock-interviews')
def mock_interviews():
    if 'user' not in session: return redirect('/login')
    return render_template('mock_interviews.html', user=session['user'])

#-----------------CREATING REGISTER PAGE--------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':# SUBMMIT FORM 
        username = request.form['username']# GET USERNAME FROM HTML PAGE 
        password = request.form['password']
        email = request.form['email']
        new_user = User(username=username, password=password, email=email) #CREATES A NEW ROW FOR NEW USER
        db.session.add(new_user)# TO INSERT DATA INTO DB
        db.session.commit()# TO SAVE THE DATA IN DB
        return redirect('/login')#AFTER REGISTER -->LOGIN PAGE
    return render_template('register.html')#JUST OPENING REGISTER FROM 

#--------------------CREATING LOGIN PAGE-------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()#to check the first match of the user in db
        if user:
            session['user'] = user.username#for storing temprarily
            return redirect('/dashboard')
        else:
            return "Invalid credentials"
    return render_template('login.html')  

# ----------------------PROFILE--------------------
@app.route('/profile',methods=['GET'])
def profile():
    return render_template('profile.html', user=session['user'],total=105)

# ----------------------FEATURES-------------------
@app.route('/features',methods=['GET','POST'])
def features():
    return render_template('features.html')


# ----------------------CONTACT--------------------
@app.route('/contact',methods=['GET','POST'])
def contact():
    return render_template('contact.html')

#----------------------LOGOUT PAGE-----------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)










