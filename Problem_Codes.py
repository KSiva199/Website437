from baseObject import baseObject

class Problem_Codes(baseObject):
    def __init__(self):
        self.setup('Problems')
    def toList(self):
        l = []
        for row in self.data:
            s = f"{row['ProblemCode']} {row['ProblemDesc']} {row['Shop']}"  
            l.append(s)
        return l
    
    def dropDownList(self):
        choices = []
        stChc = {}
        stChc['value'] = ''
        stChc['text'] = "Make A Choice"
        choices.append(stChc)
        for item in self.data:
            d = {}
            d['value'] = item[self.pk]
            d['text'] = f"{item['ProblemDesc']} ({item['ProblemCode']})"
            choices.append(d)
        return choices

    def verifyNew(self,n=0):
        if len(self.data[n]['Problem Desc']) <= 10: 
            self.errors.append('Problem Description must be longer than 10 characters')
        if len(self.data[n]['Problem Desc']) <= 5: 
            self.errors.append('Problem Code must be longer than 5 characters')
        if len(self.errors) > 0:
            return False
        else:
            return True   

    def verifyUpdt(self,n=0):
        if len(self.data[n]['Problem Desc']) <= 10: 
            self.errors.append('Problem Description must be longer than 10 characters')
        if len(self.data[n]['Problem Desc']) <= 5: 
            self.errors.append('Problem Code must be longer than 5 characters')

        if len(self.errors) > 0:
            return False
        else:
            return True