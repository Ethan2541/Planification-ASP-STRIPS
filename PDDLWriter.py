from pddl import parse_domain, parse_problem
import re

class DomainWriter(object):
    def __init__(self, domain_name):
        domain = parse_domain(domain_name)
        self.name = domain.name
        self.predicates = domain.predicates
        self.actions = domain.actions

    def write_predicates(self):
        predicates = ""
        for p in self.predicates:
            names = [t.name.upper() for t in p.terms]
            types = [f"{sorted(t.type_tags)[0]}({t.name.upper()})" for t in p.terms]
            if len(names) > 0:
                predicates += f"pred({p.name}({', '.join(names)})) :- {', '.join(types)}.\n"
            else:
                predicates += f"pred({p.name}).\n"
        return predicates

    def write_actions(self):
        actions = ""
        for a in self.actions:
            names = [t.name.upper() for t in a.parameters]
            types = [f"{sorted(t.type_tags)[0]}({t.name.upper()})" for t in a.parameters]
            if len(names) > 0:
                actions += f"action({a.name}({', '.join(names)})) :- {', '.join(types)}.\n"
            else:
                actions += f"action({a.name}).\n"
        return actions
    
    # TODO
    def write_preconditions(self):
        preconditions = ""
        for a in self.actions:
            for p in a.precondition.operands:
                try:
                    names = [t.name.upper() for t in p.terms]
                    types = [f"{sorted(t.type_tags)[0]}({t.name.upper()})" for t in p.terms]
                except:
                    p.argument
                else:
                    preconditions += f"pre({a.name}, {p.name.upper()}).\n"
        preconditions += ":- perform(A,T), pre(A,C), not holds(C,T), time(T).\n"
        return preconditions
    
    # TODO
    def write_positive_effects(self):
        positive_effects = ""
        positive_effects += "holds(F,T+1) :- perform(A,T), add(A,F).\n"
        return positive_effects

    # TODO
    def write_negative_effects(self):
        negative_effects = ""
        negative_effects += "holds(F,T+1) :- holds(F,T), perform(A,T), not del(A,F), time(T).\n"
        return negative_effects

    def write(self):
        lines += "% Declaration des predicats\n\n" + self.write_predicates()
        lines += "\n\n% Declaration des actions\n\n" + self.write_actions()
        lines += "\n\n% Preconditions\n\n" + self.write_preconditions()
        lines += "\n\n% Effets positifs\n\n" + self.write_positive_effects()
        lines += "\n\n% Effets negatifs\n\n" + self.write_negative_effects()
        return lines



class ProblemWriter(object):
    def __init__(self, problem_name):
        problem = parse_problem(problem_name)
        self.objects = problem.objects
        self.init = problem.init
        self.goal = problem.goal

    def write_objects(self):
        objects = ""
        for o in self.objects:
            pass
        return objects
    
    def write_init(self):
        init = ""
        for i in self.init:
            pass
        return init
    
    def write_goal(self):
        goal = ""
        for g in self.goal:
            pass
        return goal


    def write(self, filename):
        with open(filename, "w") as f:
            pass



class PDDLWriter(object):
    def __init__(self, domain_name, problem_name):
        self.domain = DomainWriter(domain_name)
        self.problem = ProblemWriter(problem_name)

    def write(self, filename, n):
        with open(filename, "w") as f:
            f.write(f"#const n = {n}.\ntime(0..n).")
            f.write(self.domain.write(filename))
            f.write(self.problem.write(filename))
            f.write("\n\n% Choix d'action\n\n" + "1{perform(A,T): action(A)}1 :- time(T), time(T+1).\n")
            f.write("\n\n#show holds/2.\n")



if __name__ == "__main__":
    domain = DomainWriter("./pddl_examples/domain.pddl")
    print(domain.write_preconditions())