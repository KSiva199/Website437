from baseObject import baseObject

class Problem_Codes(baseObject):
    def __init__(self):
        self.setup('PROBLEM_CODES')
    def toList(self):
        l = []
        for row in self.data:
            s = f"{row['Problem Code']} {row['Problem Description']} {row['Shop']}"  
            l.append(s)
        return l