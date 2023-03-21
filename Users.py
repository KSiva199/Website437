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