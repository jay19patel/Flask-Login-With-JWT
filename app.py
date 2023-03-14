

from flask import Flask,render_template,request,session,redirect,url_for,flash
from pymongo import MongoClient # mongodb 
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required,JWTManager,set_access_cookies
from datetime import timedelta
import requests

app = Flask(__name__)

app.secret_key = 'jaypateltopsecret789654123'
app.config["JWT_SECRET_KEY"] = "jaypateltopsecret789654123" 
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=60) 
jwt = JWTManager(app)

client = MongoClient('localhost', 27017) # connection 
db = client.Website # create table
regapi = db.Userdata # triger

@app.route('/login',methods=['GET','POST'])
def LoginPage():
    error =None
    if request.method == "POST":
        email=request.form['loginemail']
        pwd=request.form['loginpss']
        userdata=regapi.find_one({'email':email})
        if not userdata:
            flash("Email id not Founed Please Check Email id ")
            return redirect(url_for('LoginPage'))
        else:
            print("encripted  password:",userdata['password']) 
            print("real password:",pwd) 
            newpwd = pwd[::-1]+pwd[::-1]+pwd
            if userdata['password'] == newpwd:
                print("login done ....")
                access_token = create_access_token(identity=(
                    {'name':userdata['name'],
                     'city':userdata['city'],
                     'email':userdata['email']}
                     )
                    )
                # access_token = create_access_token(identity='Sallubhai')
                res = redirect(url_for('HomePage'))
                set_access_cookies(res, access_token) 
                session['login_user'] = userdata['name']
                print("Loged in......")     
                return res
               

            else:
                flash('Email & Password not match')
                return redirect(url_for('LoginPage'))

    
    return render_template('LoginPage.html')





@app.route('/logout',methods=['GET','POST'])
@jwt_required()
def Logout():
    session.clear()
    session['login_user']=''
    print("loged out...")
    flash("You are logout Login New ID ")
    return redirect(url_for('HomePage'))



@app.route('/register',methods=['GET','POST'])
def RegistrationPage():
    if request.method == "POST":
        name=request.form['fullname']
        city=request.form['mycity']
        email=request.form['myemail']
        pwd1=request.form['pass1']
        pwd2=request.form['pass2']
        print(name,city,email)
        if pwd1==pwd2:
            newpwd = pwd1[::-1]+pwd1[::-1]+pwd1
            senddata = regapi.insert_one({
                "name":name,
                "city":city,
                "email":email,
                "password":newpwd
            })
            flash('You were successfully Register Your Data')
            print("Registration Success......")  
            return redirect(url_for('LoginPage'))


        else:
            flash('Some kind of MisMatch Please Check Data')
            return redirect(url_for('RegistrationPage'))

    return render_template('RegistrPage.html')


@app.route("/" ,methods=["GET"])
def HomePage():
    session['login_user']= {'login':False}
    if 'name' in session['login_user']:
        name = session['login_user']
        print(name)
        return render_template('Home.html',name=name)
    else:
        return render_template('Home.html')

   

@app.route('/test')
@jwt_required()
def TestPage():
    if session['login_user']:
        print("Loged in Test......")  
        data = get_jwt_identity()
        name = data['name']
        email = data['email']
        city = data['city']
        print(session['login_user'])
        return render_template('Test.html',name=name,email=email,city=city)
    else:
        print(" Not Loged in......") 
        flash("You are not Log in, Login and then use TEST Page ")
        return redirect(url_for('LoginPage'))
    



@app.errorhandler(404)
def error404(error=None):
    return "<h1>Page Not Found</h1>"


# _______run_________________
if __name__=='__main__':
    app.run(debug=True)