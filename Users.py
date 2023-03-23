from baseObject import baseObject

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
        
    def verify_new(self,n=0):
        u = Users()
        u.getByField('email',self.data[n]['email'])
        if len(u.data) > 0:
            self.errors.append('Email already in use.')
        if len(self.data[n]['password']) < 2:
            self.errors.append('Password must be > 1 chars.')
        else:
            self.data[n]['password'] = self.hashPassword(self.data[n]['password'])
        if len(self.errors ) == 0:
            return True
        else:
            return False

    def verify_update(self,n=0):
        if self.data[n]['email'] == '':
            self.errors.append('Email cannot be blank.')
        if '@' not in self.data[n]['email']:
            self.errors.append('Email must contain @.')
        u = Users()
        u.getByField('email',self.data[n]['email'])
        if len(u.data) > 0 and u.data[0]['id'] != self.data[n]['id']:
            self.errors.append('Email already in use.')     
        if len(self.data[n]['password']) > 0: #user intends to change pw
            if self.data[n]['password'] != self.data[n]['password2']:
                self.errors.append('Retyped password must match.')
            if len(self.data[n]['password']) < 5:
                self.errors.append('Password must be > 4 chars.')
            else:
                self.data[n]['password'] = self.hashPassword(self.data[n]['password'])
        else:
            del self.data[n]['password']
              
        if len(self.errors ) == 0:
            return True
        else:
            return False 