from unicodedata import name
from flask import Flask,render_template, request,session, template_rendered,url_for,redirect,logging
from importlib_metadata import method_cache
from DB import db_retrive
from forms import RegisterForm
from forms import Login
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func
from passlib.hash import sha256_crypt


app=Flask(__name__) #WSGI WebService Gateway Interface 

data=db_retrive() 

#Data Base Connection
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:root@localhost/testFlaskProject"#flask_crud"

# app.config['SQLALCHEMY_BINDS']={
#     'database1':"mysql+pymysql://root:root@localhost/ITI3",
#     'database2':"mysql+pymysql://root:root@localhost/ITI4"
# }
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#object DB
db=SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(250), nullable=True)
    username = db.Column(db.String(250), nullable=True)
    email = db.Column(db.String(250), nullable=True)
    password = db.Column(db.String(250), nullable=True)
    date = db.Column(db.DateTime(timezone=True),nullable=False,server_default=func.now())
    admin =db.Column(db.Integer,nullable=True,)

    def __init__(self, name, username,email, password,date=" ",admin=0):
        self.name = name
        self.username = username
        self.email=email
        self.password = password
        if date != " " :
            self.daظte = date
        if admin != 0 :
            self.admin = admin
        

        
def add_user(name,username,email,passwd):
    #Create New ROW (New BOOK)
        enc_passwd=sha256_crypt.encrypt(passwd)
        db.create_all()
        new_user = Users(name,username,email,enc_passwd)
        db.session.add(new_user)
        db.session.commit()

@app.route('/')
# def index():
    # return "<h1>Hello Mina</h1>" #ٌٌResponce
    # home="Marco"
    # return render_template('index.html',var=home) #Responce
@app.route('/home')
def home():
    # return "<h1>Hello Mina</h1>" #ٌٌResponce
    home="Home"
    return render_template('home.html',var=home) #Responce
@app.route('/test')
def test():
    # return "<h1>Hello Mina</h1>" #ٌٌResponce
    test="test"
    return render_template('test.html',var=test) #Responce


@app.route('/about')
def about():
    # return "<h1>Hello Mina</h1>" #ٌٌResponce
    return render_template('about.html')#Responce


@app.route('/articles')
def article():
    # return "<h1>Hello Mina</h1>" #ٌٌResponce
    return render_template('articles.html',articles=data)#Responce

@app.route('/articles/<string:id>')
def article_detailes(id):
    # return "<h1>Hello Mina</h1>" #ٌٌResponce
    return render_template('articlesDetailes.html',id=id)#Responce

@app.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        #get Data From the Forms
        name=form.name.data
        username=form.username.data
        email=form.email.data
        password=form.password.data
        #Save Data in DataBase
        print(f"name={name},username={username},email={email},password={password}")
        add_user(name,username,email,password)
        #add Session 
        session["username"]=username
        session["logged_in"]=True
        return redirect(url_for("home"))
    return render_template('register.html',form=form)#Responce

@app.route('/login',methods=['GET','POST'])
def login():
    # check methods
    if request.method == "POST":
        username=request.form['username']
        password=request.form['password']
        print(f"username={username}  password= {password}")
        user = Users.query.filter_by(username=username).first()
        if(user != None):
            print(f"User = {user} userID={user.id} username={user.username} password={user.password}")
            # verify password
            if sha256_crypt.verify(password,user.password):
                session["username"]=username
                session["logged_in"]=True
                print ("Correct Password")
                return redirect(url_for("home"))

            else :
                error="The Password not match"
                return render_template('login.html',error=error)

        else:
            print ("Sorry User Not Found ")
            error="The Username not match"
            return render_template('login.html',error=error)
    return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.secret_key="@!1234"
    app.run(debug=True)


