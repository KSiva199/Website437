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
    
    def getByReqID(self,id):
        sql = f"Select * from `{self.tn}` where `RequesterID` = %s ORDER BY `WorkOrderID` DESC" 
        self.cur.execute(sql,(id))
        self.data = []
        for row in self.cur:
            self.data.append(row)

    def getAllWOs(self):
        sql = '''SELECT `WorkOrders` . * , Reqs.`UserFirstName` AS RFName, Reqs.`UserLastName` AS RLName, `Assets`.`AssetTag`, Techs.`UserFirstName` AS TFName, Techs.`UserLastName` AS TLName
        FROM `WorkOrders`
        LEFT JOIN `Users` Reqs ON `WorkOrders`.`RequesterID` = Reqs.`UserID`
        LEFT JOIN `Users` Techs ON `WorkOrders`.`TechnicianID` = Techs.`UserID`
        LEFT JOIN `Assets` ON `WorkOrders`.`AssetID` = `Assets`.`AssetID`
        LEFT JOIN `Problems` ON `WorkOrders`.`ProblemID` = `Problems`.`ProblemID`
        ORDER BY `WorkOrderID` DESC''' 
        self.cur.execute(sql)
        self.data = []
        for row in self.cur:
            self.data.append(row)
    

    def getByTechID(self,id):
        sql = f"Select * from `{self.tn}` where `TechnicianID` = %s AND `Status` = 'Open' ORDER BY `WorkOrderID` DESC" 
        self.cur.execute(sql,(id))
        self.data = []
        for row in self.cur:
            self.data.append(row)
        self.getFKMult()

    def getFKMult(self):
        newData = self.data
        self.data = []
        newFKData = []
        for n in newData:
            self.data.append(n)
            currID = n['WorkOrderID']
            self.getWOFKs(currID)
            newFKData.append(self.data[0])
            self.data = []
        for ln in newFKData:
            self.data.append(ln)
            
    
    def getByWOID(self,id): #field,value
        sql = f"SELECT * FROM `{self.tn}` WHERE `WorkOrderID` = %s" 
        self.cur.execute(sql,(id))
        self.data = []
        for row in self.cur:
            self.data.append(row) 

    def getWOFKs(self,id):
        #print(self.data)
        fkList = ['RequesterID','ProblemID','AssetID','TechnicianID']
        for fk in fkList:
            val = self.data[0][fk]
            sql=''
            #print(fk,"is",val)
            if val is not None:
                if fk == 'RequesterID':
                    sql = f"SELECT `UserID`,`UserFirstName` AS `RFName`, `UserLastName` AS `RLName` FROM `Users` WHERE `UserID` = %s"
                elif fk == 'TechnicianID':
                    sql = f"SELECT `UserID`,`UserFirstName` AS `TFName`, `UserLastName` AS `TLName` FROM `Users` WHERE `UserID` = %s"
                elif fk == 'AssetID':
                    sql = f"SELECT `AssetID` AS EqID,`AssetTag` AS `Asset`, `AssetType` FROM `Assets` WHERE `AssetID` = %s"
                else:
                    sql = f"SELECT `ProblemID`,`ProblemDesc` AS `ProbDesc`, `ProblemCode` AS `PCode` FROM `Problems` WHERE `ProblemID` = %s"
                #print(sql)
                self.cur.execute(sql,(val))
                for row in self.cur:
                    for key, value in row.items():
                        if key[-2:] != 'ID':
                            self.data[0][key] = value
        #print(self.data)
    
    def dropDownList(self):
        choices = []
        for item in self.data:
            d = {}
            d['value'] = item[self.pk]
            d['text'] = f"{item['self.pk']}: ({item['RequestDate']}, {item['Issue'][:20]})"
            choices.append(d)
        return choices
    
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
