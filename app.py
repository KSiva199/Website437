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
@app.route('/')  #route name
def home(): #view function
    return 'homepage'

    
@app.route('/confirm',methods=['GET','POST'])
def confirm():
    #product = request.form.get('product')
    product = session['product']
    ship = request.form.get('ship')
    return render_template('confirm.html',product=product,ship=ship)

#test setting a session:
@app.route('/set')
def set():
    session['key'] = 'value'
    return 'ok'

#test getting a session:
@app.route('/get')
def get():
    return session.get('key', 'not set')

@app.route('/test')
def test():
    user = 'Tommy'
    return render_template('test.html',username = user)

@app.route('/list_users')
def list_users():
    o = Users()
    o.getAll()
    return render_template('list_users.html',objs = o)

@app.route('/users/manage',methods=['GET','POST'])
def manage_user():
    o =Users()
    action = request.args.get('action')
    pkval = request.args.get('pkval')
    if action is not None and action == 'insert':
        d = {}
        d['User FN'] = request.form.get('User FN')
        d['User LN'] = request.form.get('User LN')
        d['User Username'] = request.form.get('role')
        d['Password'] = request.form.get('password')
        d['Phone Number'] = request.form.get('Phone Number')
        d['Role'] = request.form.get('Role')
        d['Shop'] = request.form.get('Shop')
        o.set(d)
        o.insert()
    if action is not None and action == 'update':
        o.getById(pkval)
        o.data[0]['User FN'] = request.form.get('User FN')
        o.data[0]['User LN'] = request.form.get('User LN')
        o.data[0]['User Username'] = request.form.get('User Username')
        o.data[0]['password'] = request.form.get('password')
        o.data[0]['Phone Number'] = request.form.get('Phone Number')
        o.data[0]['Role'] = request.form.get('Role')
        o.data[0]['Shop'] = request.form.get('Shop')
        o.update()
        
    if pkval is None:
        o.getAll()
        return render_template('users/list.html',objs = o)
    if pkval == 'new':
        o.createBlank()
        return render_template('users/add.html',obj = o)
    else:
        o.getById(pkval)
        return render_template('users/manage.html',obj = o)

#display form   
@app.route('/enterName')
def enterName():
    return render_template('nameForm.html')

#process form   
@app.route('/submitName',methods=['GET','POST'])
def submitName():
    username = request.form.get('myname')
    othername = request.form.get('othername')
    print(othername)
    print(username)
    #At this point we would INSERT the user's name to the mysql table
    return render_template('message.html',msg='name '+str(username)+' added!')

@app.route('/elements')
def elements():
    return render_template('formelements.html')

# endpoint route for static files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)
      
  
if __name__ == '__main__':
   app.run(host='127.0.0.1',debug=True)  