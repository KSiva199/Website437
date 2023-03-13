from baseObject import baseObject

class WO_Communication(baseObject):
    def __init__(self):
        self.setup('WORK ORDER COMMUNICATIONs')
    def toList(self):
        l = []
        for row in self.data:
            s = f"{row['Communication Date']} {row['Requester Message']} {row['Technician Message']} {row['WorkOrderID']}  {row['RequesterID']} {row['TechnicianID']}"  
            l.append(s)
        return l
    def getByWOCommID(self,id): #field,value
        sql = f"Select * from `{self.tn}` where `WOCommID` = %s" 
        self.cur.execute(sql,(id))
        self.data = []
        for row in self.cur:
            self.data.append(row) 