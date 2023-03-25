from baseObject import baseObject

class WO(baseObject):
    def __init__(self):
        self.setup('WorkOrders')
    def toList(self):
        l = []
        for row in self.data:
            s = f"{row['RequestDate']} {row['Issue']} {row['Shop']} {row['Status']}  {row['LaborHours']} {row['Solution']} {row['RequesterID']} {row['ProblemID']} {row['AssetID']} {row['TechnicianID']}"  
            l.append(s)
        return l
    
    def getByWOID(self,id): #field,value
        sql = f"Select * from `{self.tn}` where `WorkOrderID` = %s" 
        self.cur.execute(sql,(id))
        self.data = []
        for row in self.cur:
            self.data.append(row) 
    
    def verifyNew(self,n=0):
        if len(self.data[n]['Issue']) <= 10: 
            self.errors.append('Problem/Issue must be longer than 10 characters')

        if len(self.errors) > 0:
            return False
        else:
            return True   

    def verifyUpdt(self,n=0):
        if len(self.data[n]['Issue']) <= 10: 
            self.errors.append('Problem/Issue must be longer than 10 characters')

        if len(self.errors) > 0:
            return False
        else:
            return True
