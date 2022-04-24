from sympy import *
class Belief:
    def __init__(self, formula):
        self.formula = None
        self.cnf_formula = None
        self.create_belief(formula)

    def create_belief(self,formula):
        try:
            self.formula = formula.lower().replace(" ","")
            self.cnf_formula = to_cnf(self.formula)
        except:
            print("Belief is not valid")

