from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, escape,send_from_directory,make_response 
from flask_session import Session
from datetime import timedelta
from Users import Users
from WO import WO
from Assets import Assets
from Problem_Codes import Problem_Codes
from WO_Communication import WO_Communication

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
    if o.data[0]['User Username']==request.form.get('User Username'):
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
        return render_template('/users/requester_option.html',user=o)
    else: 
        return render_template('/users/home.html')



@app.route('/list_wo')
def list_WO():
    wo = WO()
    wo.getAll()
    return render_template('/wo/list.html',objs = wo)

@app.route('/wo/manage',methods=['GET','POST'])
def manage_WO():
    wo = WO()
    action = request.args.get('action')
    pkval = request.args.get('pkval')
    if action is not None and action == 'insert':
        d = {}
        d['Issue'] = request.form.get('Issue')
        d['Shop'] = request.form.get('Shop')
        d['Status'] = request.form.get('Status')
        d['LaborHours'] = request.form.get('LaborHours')
        d['Solution'] = request.form.get('Solution')
        d['RequesterID'] = request.form.get('RequesterID')
        d['ProblemID'] = request.form.get('ProblemID')
        d['AssetID'] = request.form.get('AssetID')
        d['TechnicianID'] = request.form.get('TechnicianID')
        wo.set(d)
        wo.insert()
    if action is not None and action == 'update':
        wo.getById(pkval)
        wo.data[0]['Issue'] = request.form.get('Issue')
        wo.data[0]['Shop'] = request.form.get('Shop')
        wo.data[0]['Status'] = request.form.get('Status')
        wo.data[0]['LaborHours'] = request.form.get('LaborHours')
        wo.data[0]['Solution'] = request.form.get('Solution')
        wo.data[0]['RequesterID'] = request.form.get('RequesterID')
        wo.data[0]['ProblemID'] = request.form.get('ProblemID')
        wo.data[0]['AssetID'] = request.form.get('AssetID')
        wo.data[0]['TechnicianID'] = request.form.get('TechnicianID')
        wo.set(d)
        wo.update()
    
    if pkval is None:
        wo.getAll()
        return render_template('wo/list.html',objs = wo)
    if pkval == 'new':
        wo.createBlank()
        return render_template('wo/add.html',obj = wo)
    else:
        wo.getById(pkval)
        uR = Users()
        uR.getByID(wo.data['RequesterID'])
        uT = Users()
        uR.getByID(wo.data['TechnicianID'])
        a = Assets()
        a.getByID(wo.data['AssetID'])
        p = Problem_Codes()
        p.getByID9(wo.data['ProblemID'])
        return render_template('wo/manage.html',wo=wo,uR=uR,uT=uT,a=a,p=p)

if __name__ == '__main__':
   app.run(host='127.0.0.1',debug=True)  