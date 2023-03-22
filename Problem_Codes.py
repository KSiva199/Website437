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