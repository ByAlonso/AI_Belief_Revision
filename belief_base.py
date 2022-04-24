from sympy import to_cnf, Not

from belief import Belief
from copy import copy
import re
class BeliefBase:
    def __init__(self, belief_base=None):
        if belief_base:
            self.belief_base = belief_base
        else:
            self.belief_base = []


    def revision(self,belief):
        self.contract(Belief(self.negate(belief.cnf_formula)))
        print("adding new belief {}".format(belief.cnf_formula))
        self.extend(belief)

    def extend(self,belief):
        self.belief_base.append(belief)

    def contract(self,new_belief):
        if not self.belief_base:
            return
        con_new_belief = new_belief
        new_belief_base = None
        queue = [self.belief_base]
        current_belief_base = ['I AM FILLED']
        while new_belief_base is None and current_belief_base:
            current_belief_base = queue.pop(0)
            for b in current_belief_base:
                if self.resolution(con_new_belief,current_belief_base):
                    aux_belief_base = copy(current_belief_base)
                    aux_belief_base = [bb for bb in aux_belief_base if bb.cnf_formula != b.cnf_formula]
                    queue.append(aux_belief_base)
                else:
                    new_belief_base = current_belief_base
                    break
        if new_belief_base is not None:
            self.belief_base = new_belief_base
        else:
            self.clear(False)
            return

    def clear(self,verbose):
        if verbose:
            print("Are you sure you want to delete all your belief base?")
            answer = input("1.Yes\n 2.No\n").lower().replace(" ","")
            if answer == "1" or answer == "yes":
                self.belief_base.clear()
                print("Belief base erased successfully!")
        else:
            self.belief_base.clear()

    def display(self):
        for x in self.belief_base:
            print(x.formula,"CNF->{}".format(x.cnf_formula))


    def resolution(self,belief,belief_base):
        '''
        Figure 7.12 A simple resolution algorithm for propositional logic. The function
        PL-RESOLVE returns the set of all possible clauses obtained by resolving its two inputs.

        :param belief:
        :return:
        '''
        new_belief = belief
        contradiction_belief = Belief(self.negate(new_belief.cnf_formula))
        clauses = [str(b.cnf_formula) for b in belief_base]
        clauses += [cb for cb in str(contradiction_belief.cnf_formula).replace(" ","").split("&")]
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
        ci_cj_pairs = [(i, j) for i in sub_ci for j in sub_cj]

        for ci_,cj_ in ci_cj_pairs:
            if ci_ == str(Not(cj_)):
                removed_ci = list(filter(lambda x: x != ci_,sub_ci))
                removed_cj = list(filter(lambda x: x != cj_,sub_cj))
                resolved_clauses.append("|".join(list(set(removed_ci + removed_cj))))
        return resolved_clauses

    def negate(self,formula):
        return "~(" + str(formula) + ")"