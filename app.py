from hashlib import sha256
from flask import Flask, redirect,request,render_template, session
from utils import Users

app = Flask(__name__, template_folder="temps")
app.secret_key = sha256("eren1234".encode()).hexdigest() 

users = Users()

@app.route('/')
def hello_world():
    if not session.get("username") or not session.get("password") or not session.get("email"):
        return render_template("login.html")
    return redirect("/home")
database={'eren':'123','osman':'123','ahmet':'123','mahmut':'456'}

@app.route("/home")
def get_home():
    username = session["username"]
    return render_template('home.html',name=username)
@app.route('/form_register',methods=['POST','GET'])
def signup():
    name = request.form.get("name", "")
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    email = request.form.get("email", "")
    from random import randint
    x,y = randint(1, 10) , randint(1, 10)
    answer = x+y
    if not request.form.get("useranswer"):
        session["security_question_answer"] = answer
    else:
        session.pop("security_question_answer")
    useranswer = int(request.form.get("useranswer", 0))
    if request.form.get("useranswer") and session.get("security_question_answer", 0) and not int(session.get("security_question_answer", 0)) == useranswer:
        return "Yanlıs cevap"
    if (not name or not username or not password or not email) and not request.method == "GET":
        return render_template("signup.html", question=f"{x} + {y} = ?", action="/form_register")

    if request.method == "POST":
        users.add_user(name, email, username, password)
        session.update(dict(name=name, email=email, username=username, password=password))
    if session.get("name"):
        return "Hello %s" % session.get("name")
    
    return render_template("signup.html", question=f"{x} + {y} = ?", action="/form_register")

@app.route("/form_logout")
def logout_security_check():
    from random import randint
    x,y = randint(1, 10) , randint(1, 10)
    answer = x+y
    session["security_question_answer"] = answer
    return render_template("captcha.html", question=f"{x} + {y} = ?", action="/verify")


@app.route("/verify", methods=["GET", "POST"])
def logout():
    answer = int(request.form.get("useranswer", 0))
    if session.get("security_question_answer", 0) and not int(session.get("security_question_answer", 0)) == answer:
        return "Yanlıs cevap"

    s = session.copy()
    for k,v in s.items():
        session.pop(k)
    return "You can log in now, click <a href='%s'>here</a>" % "/form_login"
@app.route('/form_login',methods=['POST','GET'])
def login():
        if request.method == "GET":
            if not session.get("username"):
                return "Nobody logged in!"
            return redirect("/home")
        username=request.form['username']
        password=request.form['password']
        email=request.form['email']
        if username not in database:
            return render_template('login.html',info='Invalid User')
        else:
            if database[username]!=password:
                return render_template('login.html',info='Invalid Password')
            else:
                session["username"] = username
                session["password"] = password
                session["email"] = email
                return redirect("/home")

if __name__ == '__main__':
    app.run()
