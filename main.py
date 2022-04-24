from belief import Belief
from belief_base import BeliefBase
if __name__ == '__main__':
    #Create an agent
    #Display menus
    belief_base = BeliefBase()
    while True:
        print("Possible actions:")
        print("1. Add")
        print("2. Display")
        print("3. Clear")
        print("4. Quit")
        action = input("Insert the action").lower().replace(" ","")
        if action == "quit" or action == "4":
            break
        elif action == "add" or action == "1":
            new_belief = Belief(input())
            if new_belief.cnf_formula is not None:
                belief_base.revision(new_belief)
            belief_base.display()
        elif action == "display" or action == "2":
            belief_base.display()
        elif action == "clear" or action == "3":
            belief_base.clear(True)
        else:
            print("Action not recognized, try again.")
