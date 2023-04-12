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
        for item in self.data:
            d = {}
            d['value'] = item[self.pk]
            d['text'] = f"{item['ProblemDesc']} ({item['ProblemCode']})"
            choices.append(d)
        return choices