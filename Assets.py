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
        choices.append({'value': None,'text': 'Please Choose An Asset'})
        for item in self.data:
            d = {}
            d['value'] = item[self.pk]
            d['text'] = f"{item['AssetTag']}-({item['AssetType']})"
            choices.append(d)
        return choices
    
    def uParentDDList(self):
        choices = []
        l = {'value': None,'text': 'Please Choose Parent Asset'}
        x=[]
        tmp = []
        for item in self.data:
            if item['ParentAsset'] not in tmp:
                tmp.append(item['ParentAsset'])
                d = {}
                d['value'] = item['ParentAsset']
                d['text'] = f"{item['ParentAsset']}"
                x.append(d)
            else:
                continue
        x.sort(key=lambda k : k['text'])
        choices.append(l)
        for i in x:
            choices.append(i)
        return choices
    
    def uTypeDDList(self):
        choices = []
        l = {'value': None,'text': 'Please Choose An Asset Type'}
        x=[]
        tmp = []
        for item in self.data:
            if item['AssetType'] not in tmp:
                tmp.append(item['AssetType'])
                d = {}
                d['value'] = item['AssetType']
                d['text'] = f"{item['AssetType']}"
                x.append(d)
            else:
                continue
        x.sort(key=lambda k : k['text'])
        choices.append(l)
        for i in x:
            choices.append(i)
        return choices