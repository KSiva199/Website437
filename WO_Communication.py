from baseObject import baseObject

class WO_Communication(baseObject):
    def __init__(self):
        self.setup('WorkOrderComms')
    def toList(self):
        l = []
        for row in self.data:
            s = f"{row['CommDate']} {row['Message']} {row['WorkOrderID']}  {row['UserID']}"  
            l.append(s)
        return l
    def getByWOCommID(self,id): #field,value
        sql = f"Select * from `{self.tn}` where `WOCommID` = %s" 
        self.cur.execute(sql,(id))
        self.data = []
        for row in self.cur:
            self.data.append(row) 