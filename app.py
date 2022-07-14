from unicodedata import name
from flask import Flask, flash,render_template, request,session, template_rendered,url_for,redirect,logging
from importlib_metadata import method_cache
from DB import db_retrive
from forms import RegisterForm
# from forms import 
from forms import Add_Article_form
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from passlib.hash import sha256_crypt
from sqlalchemy import desc ,asc
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
    username = db.Column(db.String(250),unique=True ,nullable=True)
    email = db.Column(db.String(250),unique=True,nullable=True)
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
class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(250), nullable=True)
    author= db.Column(db.String(250), nullable=True)
    content=db.Column(db.Text)
    created = db.Column(db.DateTime(timezone=True),nullable=False,server_default=func.now())
    approve =db.Column(db.Integer,nullable=True,)

    def __init__(self, title,author, content,created=" ",approve=0):
        self.title = title
        self.author=author
        self.content=content
        if created != " " :
            self.created = created
        # if approve != 0 :
        self.approve = approve






def add_user(name,username,email,passwd):
    #Create New ROW (New User)
        enc_passwd=sha256_crypt.encrypt(passwd)
        db.create_all()
        new_user = Users(name,username,email,enc_passwd)
        db.session.add(new_user)
        db.session.commit()

def add_article(title,author,content):
        #Create New ROW (New Article)
        db.create_all()
        new_article = Articles(title,author,content)
        db.session.add(new_article)
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
    #someselect.order_by(desc(table1.mycol))
        articles = Articles.query.filter_by(approve=0).order_by(desc(Articles.id))
        print(f"type of Article ={type(articles)},articles={articles}")

        for article in articles:
            print(f"type of Article ={type(article)}")
            print(f"Article = {article} articleID={article.id} articleTitle={article.title}")
        if(articles != [] ):
            return render_template('articles.html',articles=articles)#Responce
        else:
            #Empty Article
            msg="Error Sorry Not found Article"
            return render_template('articles.html',msg=msg)#Responce


# Create Articles 
@app.route('/create',methods=['GET','POST'])
def article_create():
    form=Add_Article_form(request.form)
    if request.method == "POST" and form.validate():
        #get Data From the Forms
        title=form.title.data
        content=form.content.data
        author=session["username"]
        add_article(title,author,content)
        print ("___________add new Article_______________")
        return redirect(url_for("article"))#show Articles
    return render_template('createArticle.html',form=form)
    
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


