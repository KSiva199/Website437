from baseObject import baseObject
import hashlib

class Users(baseObject):
    def __init__(self):
        self.setup('Users')
    def toList(self):
        l = []
        for row in self.data:
            s = f"{row['UserFirstName']} {row['UserLastName']} {row['Username']} {row['PhoneNumber']}{row['User Location']} "  
            l.append(s)
        return l
    def getByUsername(self,name): #field,value
        sql = f"Select * from `{self.tn}` where `Username` = %s" 
        self.cur.execute(sql,(name))
        self.data = []
        for row in self.cur:
            self.data.append(row)
        
    def hashPassword(self,pw):
        pw = pw+'xyz'
        return hashlib.md5(pw.encode('utf-8')).hexdigest()
    
    def verify_new(self,n=0):
        
        if self.data[n]['Username'] == '':
            self.errors.append('Email cannot be blank.')
        if '@' not in self.data[n]['Username']:
            self.errors.append('Email must contain @.')
        u = Users()
        u.getByField('Username',self.data[n]['Username'])
        if len(u.data) > 0:
            self.errors.append('Email already in use.')
        if self.data[n]['Password'] != self.data[n]['Password2']:
                self.errors.append('Re-typed password must match.')
        if len(self.data[n]['Password']) < 4:
            self.errors.append('Password must be greater than 4 chars.')
        else:
            self.data[n]['Password'] = self.hashPassword(self.data[n]['Password'])
        if len(self.errors ) == 0:
            return True
        else:
            return False
        
    def verify_update(self,n=0):
        u = Users()
        u.getByField('Username',self.data[n]['Username'])
        if len(self.data[n]['Password']) > 0: #user intends to change pw
            if self.data[n]['Password'] != self.data[n]['Password2']:
                self.errors.append('Retyped password must match.')
            if len(self.data[n]['Password']) < 5:
                self.errors.append('Password must be > 4 chars.')
            else:
                self.data[n]['Password'] = self.hashPassword(self.data[n]['Password'])
        else:
            del self.data[n]['Password']
              
        if len(self.errors ) == 0:
            return True
        else:
            return False 
        
    def tryLogin(self, Username, Password):
        hpw = self.hashPassword(Password)
        
        sql = f"SELECT * FROM `{self.tn}` WHERE `Username` = %s AND `Password` = %s;"
        #print(sql,Username,Password,hpw)
        self.cur.execute(sql,(Username,hpw))
        self.data = []
        for row in self.cur:
            self.data.append(row)
        if len(self.data) == 1:
            return True
        else:
            return False
    
    def dropDownList(self):
        choices = []
        stChc = {}
        stChc['value'] = ''
        stChc['text'] = "Make A Choice"
        choices.append(stChc)
        for item in self.data:
            d = {}
            d['value'] = item[self.pk]
            d['text'] = f"{item['UserFirstName']} {item['UserLastName']}"
            choices.append(d)
        return choices