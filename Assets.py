from baseObject import baseObject

class Assets(baseObject):
    def __init__(self):
        self.setup('Assets')
    def toList(self):
        l = []
        for row in self.data:
            s = f"{row['Parent Asset']} {row['Room Number']} {row['Asset Type']}"  
            l.append(s)
        return l
    def getByAsset(self,name): #field,value
        sql = f"Select * from `{self.tn}` where `name` = %s" 
        self.cur.execute(sql,(name))
        self.data = []
        for row in self.cur:
            self.data.append(row)
    
    def dropDownList(self):
        choices = []
        stChc = {}
        stChc['value'] = ''
        stChc['text'] = "Make a Choice"
        choices.append(stChc)
        for item in self.data:
            d = {}
            d['value'] = item[self.pk]
            d['text'] = f"{item['AssetTag']}-({item['AssetType']})"
            choices.append(d)
        return choices
    
    
