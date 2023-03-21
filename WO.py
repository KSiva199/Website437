from baseObject import baseObject

class WO(baseObject):
    def __init__(self):
        self.setup('WorkOrders')
    def toList(self):
        l = []
        for row in self.data:
            s = f"{row['Request Date']} {row['Issue']} {row['Shop']} {row['Status']}  {row['Labor Hours']} {row['Solution Notes']} {row['Requester']} {row['Problem Code']} {row['Asset']} {row['Assigned Tech']}"  
            l.append(s)
        return l
    def getByWOID(self,id): #field,value
        sql = f"Select * from `{self.tn}` where `WorkOrderID` = %s" 
        self.cur.execute(sql,(id))
        self.data = []
        for row in self.cur:
            self.data.append(row) 