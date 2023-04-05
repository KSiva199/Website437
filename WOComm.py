from baseObject import baseObject

class WOComm(baseObject):
    def __init__(self):
        self.setup('WorkOrderComms')
    def toList(self):
        l = []
        for row in self.data:
            s = f"{row['CommDate']} {row['Message']} {row['WkOrdID']}  {row['MsgUserID']}"  
            l.append(s)
        return l

    def getByWOCommID(self,id): #field,value
        sql = f"Select * from `{self.tn}` where `WOCommID` = %s" 
        self.cur.execute(sql,(id))
        self.data = []
        for row in self.cur:
            self.data.append(row) 
    
    def getCommsByWOID(self,id): #field,value
        #print(id)
        sql = f"SELECT * FROM `{self.tn}` WHERE `WkOrdID` = %s" 
        self.cur.execute(sql,(id))
        self.data = []
        for row in self.cur:
            self.data.append(row)
        #print(self.data)
        if self.data:
            self.getFKMult()

    
    def getWOCommsFKs(self,id):
        sql = f"SELECT `UserID`,`UserFirstName` AS `FName`, `UserLastName` AS `LName` FROM `Users` WHERE `UserID` = %s"
        #print(sql)
        self.cur.execute(sql,(id))
        for row in self.cur:
            #print(row)
            for key, value in row.items():
                if key[-2:] != 'ID':
                    self.data[0][key] = value
        #print(self.data)

    def getFKMult(self):
        newData = self.data
        self.data = []
        newFKData = []
        for n in newData:
            self.data.append(n)
            currID = n['MsgUserID']
            self.getWOCommsFKs(currID)
            newFKData.append(self.data[0])
            self.data = []
        for ln in newFKData:
            self.data.append(ln)

    def verifyNew(self,n=0):
        if len(self.data[n]['Message']) <= 10: 
            self.errors.append('The Work Order Message must be longer than 10 characters.')

        if len(self.errors) > 0:
            return False
        else:
            return True   

    def verifyUpdt(self,n=0):
        if len(self.data[n]['Message']) <= 10: 
            self.errors.append('The Work Order Message must be longer than 10 characters.')

        if len(self.errors) > 0:
            return False
        else:
            return True