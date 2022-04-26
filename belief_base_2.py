from sympy import to_cnf, Not

from belief import Belief
from copy import copy, deepcopy
import re

#Just some testing I was doing yesterday
#Just some testing I was doing yesterday
#Just some testing I was doing yesterday
#Just some testing I was doing yesterday
class BeliefBase2:
    def __init__(self, belief_base=None):
        if belief_base:
            self.belief_base = belief_base
        else:
            self.belief_base = []

    def revision(self,belief):
        self.contract(self.negate_belief(belief))
        print("adding new belief {}".format(belief.formula))
        self.extend(belief)

    def extend(self,belief):
        self.belief_base.append(belief)
        [print(x.formula) for x in self.belief_base]

    def contract(self,new_belief):
        if not self.belief_base:
            return
        contradiction = True
        queue = [deepcopy(self.belief_base)]

        while contradiction:
            possible_belief_bases = []
            contradiction = False
            current_belief_base = queue.pop(0)
            print("CURRENT",current_belief_base)
            for b in current_belief_base:
                if self.resolution(current_belief_base,new_belief):
                    print("SOY CONCHA ENTRO")
                    aux_belief_base = deepcopy(current_belief_base)
                    print("PRE")
                    [print(x.formula) for x in aux_belief_base]
                    aux_belief_base = [bb for bb in aux_belief_base if bb.cnf_formula != b.cnf_formula]
                    print("POST")
                    [print(x.formula) for x in aux_belief_base]
                    queue.append(aux_belief_base)
                    contradiction = True
                else:
                    possible_belief_bases.append(current_belief_base)
                    break
            print(len(queue))
            if len(queue) > 0:
                alternative_belief_base = queue.pop(0)
                while len(alternative_belief_base) == len(possible_belief_bases[0]):
                    possible_belief_bases.append(alternative_belief_base)
                    if len(queue) > 0:
                        alternative_belief_base = queue.pop(0)
                    else:
                        break

            if possible_belief_bases == []:
                self.clear(False)
                return

            #Need plausability thingy
            self.belief_base = possible_belief_bases[0]
            print(self.belief_base)



        '''if new_belief_base is not None:
            self.belief_base = new_belief_base
        else:
            self.clear(False)
            return'''

    def resolution(self,belief_base,new_belief):
        new_belief_base = belief_base + [self.negate_belief(new_belief)]
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
                    result = split_ci_ + split_cj_
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


