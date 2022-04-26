import unittest
from belief import *
from belief_base import BeliefBase as BeliefBase

def is_subset(A, B):
    dif = A - B
    dif2 = []
    for x in dif:
        for s in x.split('&'):
            dif2.append(s)
    dif2 = set(dif2)
    return dif2.issubset(B)

class TestSum(unittest.TestCase):
    # def test_contraction_closure(self):
    #     belief_basse = BeliefBase([Belief('p'),Belief('q'),Belief('p>>q'),Belief('r')])
    #     new_belief = Belief('q')
    #     belief_basse.contract(new_belief)
    #     assert not belief_basse.resolution(new_belief,belief_basse.belief_base)

    def test_contraction_success(self):
        belief_basse = BeliefBase([Belief('p'),Belief('q'),Belief('p>>q'),Belief('r')])
        new_belief = Belief('r')
        belief_basse.contract(new_belief)
        solution = [x.formula for x in belief_basse.belief_base]
        print(solution)
        assert 'r' not in solution


    def test_contraction_inclusion(self):
        belief_basse = BeliefBase([Belief('p'),Belief('q'),Belief('p>>q'),Belief('r')])
        original_set = set([x.formula for x in belief_basse.belief_base])
        new_belief = Belief('p')
        belief_basse.contract(new_belief)
        solution_set = set([x.formula for x in belief_basse.belief_base])
        assert is_subset(solution_set, original_set)


    def test_contraction_vacuity(self):
        belief_basse = BeliefBase([Belief('p'),Belief('q'),Belief('p>>q'),Belief('r')])
        original_base = belief_basse.belief_base
        new_belief = Belief('a')
        belief_basse.contract(new_belief)
        solution_base = belief_basse.belief_base
        self.assertEqual(original_base,solution_base)


    def test_contraction_extensionality(self):
        belief_basse_1 = BeliefBase([Belief('p'),Belief('q'),Belief('q>>p'),Belief('p>>q'),Belief('r')])
        belief_basse_2 = BeliefBase([Belief('p'),Belief('q'),Belief('q>>p'),Belief('p>>q'),Belief('r')])
        new_belief_1 = Belief('q')
        new_belief_2 = Belief('p')
        belief_basse_1.contract(new_belief_1)
        belief_basse_2.contract(new_belief_2)
        solution_1 = [x.formula for x in belief_basse_1.belief_base]
        solution_2 = [x.formula for x in belief_basse_2.belief_base]
        self.assertEqual(solution_1,solution_2)

    # def test_contraction_recovery(self):#NOT CORRECT YET, NEED ORDER
    #     belief_basse = BeliefBase([Belief('p'),Belief('q'),Belief('p>>q'),Belief('r')])
    #     A = set([x.formula for x in belief_basse.belief_base])
    #     new_belief = Belief('q')
    #     belief_basse.contract(new_belief)
    #     belief_basse.extend(new_belief)
    #     B = set([x.formula for x in belief_basse.belief_base])
    #     print(A,B)
    #     assert is_subset(A, B)

    def test_conjunctive_inclusion(self): 
        belief_basse_1 = BeliefBase([Belief('p'),Belief('q'),Belief('p>>q'),Belief('r')])
        new_belief_1 = Belief('p&q')
        belief_basse_1.contract(new_belief_1)
        A = set([x.formula for x in belief_basse_1.belief_base])
        belief_basse_2 = BeliefBase([Belief('p'),Belief('q'),Belief('p>>q'),Belief('r')])
        new_belief_2 = Belief('p')
        belief_basse_2.contract(new_belief_2)
        B = set([x.formula for x in belief_basse_2.belief_base])
        print(A,B)
        assert is_subset(A, B)

    def test_conjunctive_overlap(self):#NOT CORRECT YET, NEED ORDER
        belief_basse_1 = BeliefBase([Belief('p'),Belief('q'),Belief('p>>q'),Belief('r')])
        belief_basse_2 = BeliefBase([Belief('p'),Belief('q'),Belief('p>>q'),Belief('r')])
        belief_basse_3 = BeliefBase([Belief('p'),Belief('q'),Belief('p>>q'),Belief('r')])
        new_belief_1 = Belief('p')
        new_belief_2 = Belief('q')
        new_belief_3 = Belief('p&q')
        belief_basse_1.contract(new_belief_1)
        belief_basse_2.contract(new_belief_2)
        belief_basse_3.contract(new_belief_3)
        A1 = set([x.formula for x in belief_basse_1.belief_base])
        A2 = set([x.formula for x in belief_basse_2.belief_base])
        B = set([x.formula for x in belief_basse_3.belief_base])
        print(A1,A2,B)
        assert is_subset(A1.intersection(A2), B)


    # def test_revision_closure(self):#How does this work???
    #     belief_basse = BeliefBase([Belief('p'), Belief('q'), Belief('p>>q'), Belief('r')])
    #     new_belief = Belief('~q')
    #     belief_basse.revision(new_belief)
    #     solution = [x.formula for x in belief_basse.belief_base]
    #     assert '~q' in solution

    def test_revision_success(self):
        belief_basse = BeliefBase([Belief('p'), Belief('q'), Belief('p>>q'), Belief('r')])
        new_belief = Belief('~q')
        belief_basse.revision(new_belief)
        solution = [x.formula for x in belief_basse.belief_base]
        assert '~q' in solution

    def test_revision_inclusion(self):
        belief_basse_1 = BeliefBase([Belief('p'), Belief('q'), Belief('p>>q'), Belief('r')])
        new_belief_1 = Belief('~q')
        belief_basse_1.revision(new_belief_1)
        A = set([x.formula for x in belief_basse_1.belief_base])
        belief_basse_2 = BeliefBase([Belief('p'), Belief('q'), Belief('p>>q'), Belief('r')])
        new_belief_2 = Belief('~q')
        belief_basse_2.extend(new_belief_2)
        B = set([x.formula for x in belief_basse_2.belief_base])
        assert is_subset(A, B)

    def test_revision_vacuity(self):
        belief_basse = BeliefBase([Belief('p'), Belief('q'), Belief('p>>q'), Belief('r')])
        new_belief = Belief('q')
        belief_basse.revision(new_belief)
        A = [x.formula for x in belief_basse.belief_base]
        belief_basse_2 = BeliefBase([Belief('p'), Belief('q'), Belief('p>>q'), Belief('r')])
        new_belief_2 = Belief('q')
        belief_basse_2.extend(new_belief_2)
        B = [x.formula for x in belief_basse_2.belief_base]
        print(A,B)
        self.assertEqual(A, B)

    def test_revision_consistency(self):
        belief_basse = BeliefBase([Belief('p'), Belief('q'), Belief('p>>q')])
        new_belief = Belief('r')
        belief_basse.revision(new_belief)
        # A = [x.formula for x in belief_basse.belief_base]
        # print(A)
        assert belief_basse.resolution(new_belief, belief_basse.belief_base)

    def test_revision_extensionality(self):
        belief_basse_1 = BeliefBase([Belief('p'),Belief('q'),Belief('q>>p'),Belief('p>>q'),Belief('r')])
        belief_basse_2 = BeliefBase([Belief('p'),Belief('q'),Belief('q>>p'),Belief('p>>q'),Belief('r')])
        new_belief_1 = Belief('q')
        new_belief_2 = Belief('p')
        belief_basse_1.revision(new_belief_1)
        belief_basse_2.revision(new_belief_2)
        solution_1 = [x.formula for x in belief_basse_1.belief_base]
        solution_2 = [x.formula for x in belief_basse_2.belief_base]
        self.assertEqual(solution_1,solution_2)

    def test_revision_superexpansion(self):
        belief_basse_1 = BeliefBase([Belief('p'),Belief('q'),Belief('q>>p'),Belief('r')])
        belief_basse_2 = BeliefBase([Belief('p'),Belief('q'),Belief('q>>p'),Belief('r')])
        new_belief_1 = Belief('t&s')
        new_belief_2 = Belief('t')
        new_belief_3 = Belief('s')
        belief_basse_1.revision(new_belief_1)
        belief_basse_2.revision(new_belief_2)
        belief_basse_2.extend(new_belief_3)
        A = set([x.formula for x in belief_basse_1.belief_base])
        B = set([x.formula for x in belief_basse_2.belief_base])

        print(A, B)
        assert is_subset(A,B)

    # def test_revision_subexpansion(self):
    #     belief_basse_1 = BeliefBase([Belief('p'),Belief('q'),Belief('p>>q')])
    #     belief_basse_2 = BeliefBase([Belief('p'),Belief('q'),Belief('p>>q')])
    #     new_belief_1 = Belief('p&q')
    #     new_belief_2 = Belief('p')
    #     new_belief_3 = Belief('q')
    #     not_belief_3 = Belief('~q')
    #     belief_basse_1.revision(new_belief_2)

    #     if not_belief_3.formula not in [x.formula for x in belief_basse_1.belief_base]:
    #         belief_basse_1.extend(new_belief_3)
    #         belief_basse_2.revision(new_belief_1)

    #         A = set([x.formula for x in belief_basse_1.belief_base])
    #         B = set([x.formula for x in belief_basse_2.belief_base])
    #         print('a')
    #         print(A, B)
    #         assert is_subset(A, B)
    #     else:
    #         print('¬ψ ∈ B ∗ φ')
    #         assert False

if __name__ == '__main__':
    unittest.main()