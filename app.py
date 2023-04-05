from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, escape,send_from_directory,make_response 
from flask_session import Session
from datetime import timedelta
from datetime import datetime
from Users import Users
from WO import WO
from Assets import Assets
from Problem_Codes import Problem_Codes
from WOComm import WOComm
import time

#create Flask app instance
app = Flask(__name__,static_url_path='')

#Configure serverside sessions 
app.config['SECRET_KEY'] = '56hdtryhRTg'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
sess = Session()
sess.init_app(app)

@app.context_processor
def inject_user():
    return dict(me=session.get('user'))

#Basic root route - show the word 'homepage'
@app.route('/home')  #route name
def home(): #view function
    if checkSession() == False: 
        return render_template('/users/home.html')
    return render_template('/users/home.html') 
    
@app.route('/register')
def register():
    u =Users()
    action = request.args.get('action')
    if action is not None and action=='new':
        return render_template('/users/add.html',obj=u)
    if action is not None and action=='update':
        pkval = request.args.get('pkval')
        u.getById(pkval)
        return render_template('/users/update.html',user=u)
    if action is not None and action=='manager_update':
        pkval = request.args.get('pkval')
        u.getById(pkval)
        return render_template('/users/updateuser_manager.html',user=u)


@app.route('/manage_user',methods=['GET','POST'])
def manage_user():
    #if checkSession() == False: 
    #    return render_template('/users/home.html', msg='Session Failed')
    action = request.args.get('action')
    pkval = request.args.get('pkval')
    if action is not None and action=='new':
        o=Users()
        d = {}
        d['UserFirstName'] = request.form.get('UserFirstName')
        d['UserLastName'] = request.form.get('UserLastName')
        d['Username'] = request.form.get('Username')
        d['Password'] = request.form.get('Password')
        d['Password2'] = request.form.get('ConfirmPassword')
        d['PhoneNumber'] = request.form.get('PhoneNumber')
        d['LocationID'] = request.form.get('LocationID')
        d['Shop'] = 'None'
        d['Role'] = 'Requester'
        o.set(d)
        if o.verify_new()==True:
            o.insert()
            return render_template('/users/home.html',msg='User Added')
        else:
            return render_template('/users/add.html', obj = o)
    if action is not None and action=='update':
        o=Users()
        o.getById(pkval)
        o.data[0]['UserFirstName'] = request.form.get('UserFirstName')
        o.data[0]['UserLastName'] = request.form.get('UserLastName')
        o.data[0]['Username'] = request.form.get('Username')
        o.data[0]['Password'] = request.form.get('Password')
        o.data[0]['Password2'] = request.form.get('ConfirmPassword')
        o.data[0]['PhoneNumber'] = request.form.get('PhoneNumber')
        if session['user']['Role'] == 'Manager':
            o.data[0]['Role'] = request.form.get('Role')
            o.data[0]['Shop'] = request.form.get('Shop')
        if o.verify_update():
            o.update()
            if session['user']['Role'] == 'Manager':
                return render_template('/users/manager_option.html', title='Main menu',user=o) 
            elif session['user']['Role']=='Technician':
                return render_template('/users/technician_option.html', title='Main menu',user=o)
            else:
                return render_template('/users/requester_option.html', title='Main menu',user=o) 

    if pkval is None:
        o.getAll()
        return render_template('users/list.html',objs = o)
    if pkval == 'new':
        o.createBlank()
        return render_template('users/add.html',obj = o)
    else:
        o.getById(pkval)
        return render_template('users/manage.html',obj = o)
    
    
@app.route('/redirect_user', methods=['GET','POST'])
def redirect_user():
    u=Users()
    if session['user']['Role'] == 'Manager':
        return render_template('/users/manager_option.html', title='Main menu',user=u) 
    elif session['user']['Role']=='Technician':
        return render_template('/users/technician_option.html', title='Main menu',user=u)
    else:
        return render_template('/users/requester_option.html', title='Main menu',user=u) 

    
@app.route('/login_user',methods=['GET','POST'])
def login_user():
    #if checkSession() == False: 
    #  return redirect('/home')
    if request.form.get('Username') is not None and request.form.get('Password') is not None:
        u = Users()
        if u.tryLogin(request.form.get('Username'),request.form.get('Password')):
            u.getById(u.data[0]['UserID'])
            #print(u.data)
            print('login ok')
            session['user'] = u.data[0]
            session['active'] = time.time()
            if session['user']['Role'] == 'Manager':
                return render_template('/users/manager_option.html', title='Main menu',user=u) 
            elif session['user']['Role']=='Technician':
                return render_template('/users/technician_option.html', title='Main menu',user=u)
            else:
                return render_template('/users/requester_option.html', title='Main menu',user=u) 
            
        else:
            print('login failed')
            return render_template('users/home.html', title='Login', msg='Incorrect username or password.')
    else:
        if 'msg' not in session.keys() or session['msg'] is None:
            m = 'Type your email and password to continue.'
        else:
            m = session['msg']
            session['msg'] = None
        return render_template('users/home.html', title='Login', msg=m)
    
    
@app.route('/logout',methods = ['GET','POST'])
def logout():
    if session.get('user') is not None:
        del session['user']
        del session['active']
    return render_template('users/home.html', title='Login', msg='You have logged out.')

# endpoint route for static files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

def checkSession():
    if 'active' in session.keys():
        timeSinceAct = time.time() - session['active']
        print(timeSinceAct)
        if timeSinceAct > 500:
            session['msg'] = 'Your session has timed out.'
            return False
        else:
            session['active'] = time.time()
            return True
    else:
        return False

@app.route('/list_users')
def list_users():
    u = Users()
    u.getAll()
    return render_template('/users/list.html',obj = u)

@app.route('/list_technician')
def list_technician():
    u = Users()
    u.getByField('Role','Technician')
    return render_template('/users/list_technician.html',obj = u)

@app.route('/list_assets')
def list_assets():
    u = Assets()
    u.getAll()
    return render_template('/assets/list_all_assets.html',obj = u)

@app.route('/register_asset')
def register_asset():
    u =Assets()
    action = request.args.get('action')
    if action is not None and action=='new':
        return render_template('/assets/add.html',obj=u)
    if action is not None and action=='update':
        pkval = request.args.get('pkval')
        u.getById(pkval)
        return render_template('/assets/manage.html',obj=u)


@app.route('/manage_asset',methods=['GET','POST'])
def manage_asset():
    #if checkSession() == False or session['user']['role'] != 'Requester': 
    #    return redirect('/home')
    action = request.args.get('action')
    pkval = request.args.get('pkval')
    if action is not None and action=='new':
        o=Assets()
        d = {}
        d['AssetID'] = request.form.get('AssetID')
        d['ParentAsset'] = request.form.get('ParentAsset')
        d['AssetTag'] = request.form.get('AssetTag')
        d['AssetType'] = request.form.get('AssetType')
        o.set(d)
        o.insert()
        return render_template('/users/manager_option.html',msg='Asset Added')
    if action is not None and action=='update':
        o=Assets()
        o.getById(pkval)
        o.data[0]['ParentAsset'] = request.form.get('ParentAsset')
        o.data[0]['AssetTag'] = request.form.get('AssetTag')
        o.data[0]['AssetType'] = request.form.get('AssetType')
        o.update()   
        return render_template('/users/manager_option.html',msg='Asset Updated')   

    if pkval is None:
        o.getAll()
        return render_template('users/list.html',objs = o)
    if pkval == 'new':
        o.createBlank()
        return render_template('assets/add.html',obj = o)
    else:
        o.getById(pkval)
        return render_template('users/manage.html',obj = o)

@app.route('/update_user', methods=['GET','POST'])
def update_user():
    o=Users()
    o.getById(o.pk)
    o.data[0]['UserFirstName'] = request.form.get('UserFirstName')
    o.data[0]['UserLasttName'] = request.form.get('UserLastName')
    o.data[0]['password'] = request.form.get('Password')
    o.data[0]['password2'] = request.form.get('ConfirmPassword')
    if o.verify_update():
        o.update()
        return render_template('/users/requester_option.html',user=o)
    
'''if pkval is None:
    o.getAll()
    return render_template('users/list.html',objs = o)
if pkval == 'new':
    o.createBlank()
    return render_template('users/add.html',obj = o)
else:
    o.getById(pkval)
    return render_template('users/manage.html',obj = o)
'''
@app.route('/main_menu')
def main_menu():
    if session['user']['Role'] == 'Manager':
        return render_template('/users/manager_option.html', title='Main Menu') 
    elif session['user']['Role']=='Technician':
        return render_template('/users/technician_option.html', title='Main Menu')
    else:
        return render_template('/users/requester_option.html', title='Main Menu')

@app.route('/wo/list_wo',methods=['GET','POST'])
def list_WO():
    wo = WO()
    pkval = session['user']['UserID']
    if session['user']['Role'] == 'Requester':
        wo.getByReqID(pkval)
        return render_template('/wo/listwo_req.html',wo=wo)
    elif session['user']['Role'] == 'Technician':
        wo.getByTechID(pkval)
        return render_template('/wo/listwo_tech.html',wo=wo)
    elif session['user']['Role'] == 'Manager':
        wo.getAllWOs()
        return render_template('/wo/listwo_mgr.html',wo=wo)
    
    #return render_template('/wo/listwo.html',wo = wo)

@app.route('/wo/manage',methods=['GET','POST'])
def manage_WO():
    wo = WO()
    action = request.args.get('action')
    pkval = request.args.get('pkval')
    if action is not None and action == 'insert':
        d = {}
        d['Issue'] = request.form.get('Issue')
        d['RequestDate'] = request.form.get('RequestDate')
        d['Shop'] = request.form.get('Shop')
        d['Status'] = request.form.get('Status')
        d['LaborHours'] = request.form.get('LaborHours')
        d['Solution'] = request.form.get('Solution')
        d['RequesterID'] = request.form.get('RequesterID')
        d['ProblemID'] = request.form.get('ProblemID')
        d['AssetID'] = request.form.get('AssetID')
        d['TechnicianID'] = request.form.get('TechnicianID')

        if d['AssetID'] is not None:
            d['AssetID'] = int(d['AssetID'])

        possEmpty = ['RequestDate','Shop','Status','LaborHours','Solution','RequesterID','ProblemID','TechnicianID']
        for p in possEmpty:
            if d[p] is None:
                if p == 'RequestDate':
                    d[p] = datetime.now().date()
                elif p == 'Status':
                    d[p] = 'Open'
                elif p == 'RequesterID':
                    d[p] = int(session['user']['UserID'])
        
        for key in d:
            if key in ['ProblemID','AssetID','TechnicianID'] and d[key] is not None:
                d[key] = int(d[key])
        #print(d)
        wo.set(d)
        if wo.verifyNew():
            wo.insert()
        else:
            return render_template('/wo/addwo.html',wo = wo)
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
        if wo.verifyUpdt():
            wo.update()
        else:
            return render_template('/wo/manage.html',wo = wo)
        
    if pkval is None:
        if session['user']['Role'] == 'Manager':
            return render_template('/users/manager_option.html', title='Main Menu') 
        elif session['user']['Role']=='Technician':
            return render_template('/users/technician_option.html', title='Main Menu')
        else:
            return render_template('/users/requester_option.html', title='Main Menu')
        #wo.getAll()
        #return render_template('/wo/listwo.html',wo = wo)
    elif pkval == 'new':
        wo.createBlank()
        if session['user']['Role'] == 'Manager':
            return render_template('wo/addwo_mgr.html',wo=wo) 
        elif session['user']['Role']=='Technician':
            return render_template('wo/addwo_tech.html',wo=wo) 
        else:
            return render_template('wo/addwo.html',wo=wo) 
        #return render_template('/wo/addwo.html',wo = wo)
    else:
        wo.getById(pkval)
        wo.getWOFKs(pkval)
        if session['user']['Role'] == 'Manager':
            return render_template('wo/wosumm_mgr.html',wo=wo) 
        elif session['user']['Role']=='Technician':
            return render_template('wo/wosumm_tech.html',wo=wo) 
        else:
            return render_template('wo/wosumm.html',wo=wo) 
        #return render_template('wo/manage.html',wo=wo)

@app.route('/wocomms/manage_comm',methods=['GET','POST'])
def manage_comm():
    o = WOComm()
    action = request.args.get('action')
    pkval = request.args.get('pkval')

    if action is not None and action == 'insert':
        d = {}
        d['Message'] = request.form.get('Message')
        d['CommDate'] = datetime.now().date()
        d['MsgUserID'] = session['user']['UserID']
        d['WkOrdID'] = session['user']['WO']
        
        o.set(d)
        if o.verifyNew():
            o.insert()
            o.getCommsByWOID(int(session['user']['WO']))
            return render_template('/wocomms/listcomms.html', comm = o)
        else:
            return render_template('wocomms/addcomm.html',obj = o)
    
    if pkval is None:
        if session['user']['Role'] == 'Manager':
            return render_template('/users/manager_option.html',msg="No Work Order Selected.") 
        elif session['user']['Role']=='Technician':
            return render_template('/users/technician_option.html',msg="No Work Order Selected.") 
        else:
            return render_template('/users/requester_option.html',msg="No Work Order Selected.") 
    if pkval == 'new':
        o.createBlank()
        return render_template('wocomms/addcomm.html',obj = o)

@app.route('/wocomms/list_comms',methods=['GET','POST'])
def list_comms():
    comm = WOComm()
    pkval = request.args.get('pkval')
    session['user']['WO'] = pkval

    if pkval is not None:
        comm.getCommsByWOID(pkval)
        print(comm.data)
        if comm.data:
            return render_template('/wocomms/listcomms.html', comm = comm)
        else:
            wkid = {}
            wkid['WkOrdID'] = pkval
            comm.data.append(wkid)
            return render_template('/wocomms/listcomms_emp.html', comm = comm)

if __name__ == '__main__':
   app.run(host='127.0.0.1',debug=True)  