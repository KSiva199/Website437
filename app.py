from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, escape,send_from_directory,make_response 
from flask_session import Session
from datetime import timedelta
from Users import Users

#create Flask app instance
app = Flask(__name__,static_url_path='')

#Configure serverside sessions 
app.config['SECRET_KEY'] = '56hdtryhRTg'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
sess = Session()
sess.init_app(app)

#Basic root route - show the word 'homepage'
@app.route('/home')  #route name
def home(): #view function
    return render_template('/users/home.html')

@app.route('/register')
def register():
    return render_template('/users/add.html')

@app.route('/manage_user',methods=['GET','POST'])
def manage_user():
    o =Users()
    d = {}
    d['User FN'] = request.form.get('User FN')
    d['User LN'] = request.form.get('User LN')
    d['User Username'] = request.form.get('User Username')
    d['Password'] = request.form.get('password')
    d['Phone Number'] = request.form.get('Phone Number')
    d['Role'] = request.form.get('Role')
    d['Shop'] = request.form.get('Shop')
    o.getByUsername(request.form.get('User Username'))
    if request.form.get('User Username')==o.data[0]['User Username']:
        return "Email address already exist"
    else: 
        o.set(d)
        o.insert()
        return render_template('/users/home.html')

@app.route('/login_user',methods=['GET','POST'])
def login_user():
    o=Users()
    o.getByUsername(request.form.get('User Username'))
    if (o.data[0]['User Username']==request.form.get('User Username')) and (o.data[0]['Password']==request.form.get('Password')) :
        return render_template('/users/demo.html',user=o)
    else: 
        return render_template('/users/home.html')



  
if __name__ == '__main__':
   app.run(host='127.0.0.1',debug=True)  