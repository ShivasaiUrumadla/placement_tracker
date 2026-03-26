
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,render_template,request,redirect,session,url_for
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
import requests

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

#---------------CREATING TABLE USING PYTHON INSTEAD OF WRTING SQL MANUALLY---------------
class dsa_questions(db.Model):
    __tablename__="dsa_questions"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(100))
    difficulty=db.Column(db.String(100))
    topic=db.Column(db.String(100))
    link=db.Column(db.String(100))

   

#--------------HOME REDIRECTS TO REGISTER-------------------------
@app.route('/')
def index():
    # Force logout if the user visits the root page so it ALWAYS shows register first
    # session.pop('user', None)
    if 'user' in session:
        return redirect('/dashboard')
    return redirect('/login')   

# ---------------ADMIN----------------------------
@app.route('/admin')
def admin():
    if 'user' not in session:
        return redirect('/login')
    return render_template('admin.html', user=session['user'])

# ------------------- ADMIN DSA TOPIC ROUTES ----------------------------
def fetch_leetcode_problems(tag, limit=20):
    url = "https://leetcode.com/graphql"
    query = {
        "query": f"""
        {{
        questionList(
            categorySlug: ""
            limit: {limit}
            skip: 0
            filters: {{
            tags: ["{tag}"]
            }}
        ) {{
            data {{
            title
            titleSlug
            difficulty
            topicTags {{
                slug
            }}
            }}
        }}
        }}
        """
    }
    try:
        res = requests.post(url, json=query, timeout=10)
        data = res.json()
        problems = data["data"]["questionList"]["data"]
        result = []
        for p in problems:
            result.append({
                "name": p["title"],
                "difficulty": p["difficulty"],
                "tags": [t["slug"] for t in p["topicTags"]],
                "link": f"https://leetcode.com/problems/{p['titleSlug']}/"
            })
        return result
    except Exception as e:
        print(f"Error fetching LeetCode problems: {e}")
        return []

@app.route('/admin/arrays')
def admin_arrays():
    if 'user' not in session: return redirect('/login')
    problems = fetch_leetcode_problems("array")
    return render_template('admin.html', user=session['user'], clean_data=problems, topic="Arrays & Strings")

@app.route('/admin/linked-list')
def admin_linked_list():
    if 'user' not in session: return redirect('/login')
    problems = fetch_leetcode_problems("linked-list")
    return render_template('admin.html', user=session['user'], clean_data=problems, topic="Linked List")

@app.route('/admin/stack-queue')
def admin_stack_queue():
    if 'user' not in session: return redirect('/login')
    problems = fetch_leetcode_problems("stack")
    return render_template('admin.html', user=session['user'], clean_data=problems, topic="Stack & Queue")

@app.route('/admin/trees')
def admin_trees():
    if 'user' not in session: return redirect('/login')
    problems = fetch_leetcode_problems("tree")
    return render_template('admin.html', user=session['user'], clean_data=problems, topic="Trees")

@app.route('/admin/graphs')
def admin_graphs():
    if 'user' not in session: return redirect('/login')
    problems = fetch_leetcode_problems("graph")
    return render_template('admin.html', user=session['user'], clean_data=problems, topic="Graphs")

@app.route('/admin/dp')
def admin_dp():
    if 'user' not in session: return redirect('/login')
    problems = fetch_leetcode_problems("dynamic-programming")
    return render_template('admin.html', user=session['user'], clean_data=problems, topic="Dynamic Programming")

@app.route('/admin/hashing')
def admin_hashing():
    if 'user' not in session: return redirect('/login')
    problems = fetch_leetcode_problems("hash-table")
    return render_template('admin.html', user=session['user'], clean_data=problems, topic="Hashing")

@app.route('/admin/sorting')
def admin_sorting():
    if 'user' not in session: return redirect('/login')
    problems = fetch_leetcode_problems("sorting")
    return render_template('admin.html', user=session['user'], clean_data=problems, topic="Sorting & Searching")

@app.route('/admin/greedy')
def admin_greedy():
    if 'user' not in session: return redirect('/login')
    problems = fetch_leetcode_problems("greedy")
    return render_template('admin.html', user=session['user'], clean_data=problems, topic="Greedy")

@app.route('/admin/backtracking')
def admin_backtracking():
    if 'user' not in session: return redirect('/login')
    problems = fetch_leetcode_problems("backtracking")
    return render_template('admin.html', user=session['user'], clean_data=problems, topic="Backtracking")

@app.route('/admin/bit-manipulation')
def admin_bit_manipulation():
    if 'user' not in session: return redirect('/login')
    problems = fetch_leetcode_problems("bit-manipulation")
    return render_template('admin.html', user=session['user'], clean_data=problems, topic="Bit Manipulation")

@app.route('/admin/math')
def admin_math():
    if 'user' not in session: return redirect('/login')
    problems = fetch_leetcode_problems("math")
    return render_template('admin.html', user=session['user'], clean_data=problems, topic="Math & Number Theory")


#--------------HANDLING DATA FROM ADMIN TO STUDENT------------------------

@app.route('/admin/add-problem',methods=['POST'])
def admin_addproblem():
    name=request.form.get('name')
    difficulty=request.form.get('difficulty')
    tags=request.form.get('tags')
    link=request.form.get('link')
    

#--------------CREATING DASHBOARD PAGE-------------------------
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    users = User.query.all()
    role = 'admin account' if session['user'].lower() == 'admin' else 'student account'
    return render_template('dashboard.html', user=session['user'], users=users, role=role)

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










