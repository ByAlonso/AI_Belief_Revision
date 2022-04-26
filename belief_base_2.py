from sympy import to_cnf, Not

from belief import Belief
from copy import copy, deepcopy
import re

#Just some testing I was doing yesterday
#Just some testing I was doing yesterday
#Just some testing I was doing yesterday
#Just some testing I was doing yesterday
class BeliefBase:
    def __init__(self, belief_base=None):
        if belief_base:
            self.belief_base = belief_base
        else:
            self.belief_base = []

    def revision(self,belief):
        if belief.cnf_formula not in [x.cnf_formula for x in self.belief_base]:
            self.contract(self.negate_belief(belief))
            print("adding new belief {}".format(belief.formula))
            self.extend(belief)

    def extend(self,belief):
        if belief.cnf_formula not in [x.cnf_formula for x in self.belief_base]:
            self.belief_base.append(belief)
        [print(x.formula) for x in self.belief_base]

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
                if self.resolution(current_belief_base,con_new_belief):
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

    def resolution(self,belief_base,new_belief):
        new_belief_base = belief_base + [self.negate_belief(new_belief)]
        [print(x.cnf_formula,",") for x in new_belief_base]
        clauses = [str(belief.cnf_formula).replace(" ","").split("&") for belief in new_belief_base]
        clauses = [sc for c in clauses for sc in c]
        new = set()
        while True:
            clauses_pair = set([(clauses[ci], clauses[cj]) for ci in range(len(clauses)) for cj in range(ci+1,len(clauses)) if ci != cj])
            for ci,cj in clauses_pair:
                resolvents = self.resolve(ci,cj)
                if '' in resolvents:
                    print("TRUE")
                    return True
                new = new.union(set(resolvents))
            if new.issubset(clauses):
                print("FALSE")
                return False
            clauses += [n for n in new if n not in clauses]

    def resolve(self,ci,cj):
        final_result = []
        split_ci = [sci.replace("(","").replace(")","") for sci in ci.replace(" ","").split('|')]
        split_cj = [scj.replace("(","").replace(")","") for scj in cj.replace(" ","").split('|')]
        for sci in split_ci:
            for scj in split_cj:
                if to_cnf(sci) == self.negate_cnf(scj) or to_cnf(scj) == self.negate_cnf(sci): #I think the or is redundant
                    split_ci_ = [x for x in split_ci if x != sci]
                    split_cj_ = [x for x in split_cj if x != scj]
                    result = list(set(split_ci_ + split_cj_))
                    final_result.append('|'.join(result))
        return final_result

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

    def negate_belief(self,belief):
        return Belief('~(' + str(belief.formula) + ')')

    def negate_cnf(self,formula):
        return to_cnf('~(' + formula + ')')


