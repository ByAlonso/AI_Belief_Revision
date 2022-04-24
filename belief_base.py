from belief import Belief
from sympy import Not
class BeliefBase:
    def __init__(self):
        self.belief_base = []
        self.absolute_beliefs = []


    def add(self,belief):
        self.belief_base.append(belief)
        self.add_absolute_belief(belief)

    def add_absolute_belief(self,belief):
        for b in belief.formula:
            if b.match('[a-zA-Z]') and b not in self.absolute_beliefs:
                self.absolute_beliefs.append(b)

    def contract(self):
        pass



    def clear(self):
        print("Are you sure you want to delete all your belief base?")
        answer = input("1.Yes\n 2.No\n").lower().replace(" ","")
        if answer == "1" or answer == "yes":
            self.belief_base.clear()
            self.absolute_beliefs.clear()
            print("Belief base erased successfully!")

    def display(self):
        for x in self.belief_base:
            print(x)

    def resolution(self,belief):
        '''
        Figure 7.12 A simple resolution algorithm for propositional logic. The function
PL-RESOLVE returns the set of all possible clauses obtained by resolving its two inputs.

        :param belief:
        :return:
        '''
        new_belief = belief
        contradiction_belief = Belief(f'({new_belief.cnf_formula})')
        clauses = [cb for cb in contradiction_belief.cnf_formula.replace(" ","").split("&")]
        clauses_set = set()
        while True:
            resolve_pairs = [(clauses[i],clauses[j]) for i in range(0,len(clauses)) for j in range(i+1,len(clauses))]
            for ci,cj in resolve_pairs:
                result = self.resolve(ci,cj)
                if '' in result:
                    return True
                clauses_set = clauses_set.union(set(result))

            if clauses_set.issubset(set(clauses)):
                return False

            for new_clause in clauses_set:
                if new_clause not in clauses:
                    clauses.append(new_clause)

    def resolve(self,ci,cj):

        resolved_clauses = []
        sub_ci = [sci for sci in ci.split("|")]
        sub_cj = [scj for scj in cj.split("|")]
        ci_cj_pairs = [(sub_ci[i], sub_cj[j]) for i in sub_ci for j in sub_cj]

        for ci_,cj_ in ci_cj_pairs:
            if ci_ == Not(cj_):
                removed_ci = list(filter(lambda x: x != ci_,sub_ci))
                removed_cj = list(filter(lambda x: x != cj_,sub_cj))
                resolved_clauses.append("|".join(list(set(removed_ci + removed_cj))))

        return resolved_clauses