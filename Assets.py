from baseObject import baseObject

class Assets(baseObject):
    def __init__(self):
        self.setup('ASSETS')
    def toList(self):
        l = []
        for row in self.data:
            s = f"{row['Parent Asset']} {row['Room Number']} {row['Asset Type']}"  
            l.append(s)
        return l
    def getByAssest(self,name): #field,value
        sql = f"Select * from `{self.tn}` where `name` = %s" 
        self.cur.execute(sql,(name))
        self.data = []
        for row in self.cur:
            self.data.append(row) 