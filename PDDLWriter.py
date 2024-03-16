from pddl import parse_domain, parse_problem
from pddl.logic import Predicate
from pddl.logic.base import Not
import re

class DomainWriter(object):
    def __init__(self, domain_name):
        domain = parse_domain(domain_name)
        self.name = domain.name
        self.predicates = domain.predicates
        self.actions = domain.actions

    def write_predicates(self):
        # On écrit les prédicats pred(P)
        predicates = ""
        for p in self.predicates:
            names = [t.name.upper() for t in p.terms]
            types = [f"{sorted(t.type_tags)[0]}({t.name.upper()})" for t in p.terms]
            # Prédicat avec arguments
            if len(names) > 0:
                predicates += f"pred({p.name}({','.join(names)})) :- {', '.join(types)}.\n"
            # Prédicat sans argument
            else:
                predicates += f"pred({p.name}).\n"
        return predicates

    def write_actions(self):
        # On écrit les prédicats action(A)
        actions = ""
        for a in self.actions:
            names = [t.name.upper() for t in a.parameters]
            types = [f"{sorted(t.type_tags)[0]}({t.name.upper()})" for t in a.parameters]
            if len(names) > 0:
                actions += f"action({a.name}({','.join(names)})) :- {', '.join(types)}.\n"
            else:
                actions += f"action({a.name}).\n"
        return actions
    
    def write_preconditions(self):
        preconditions = ""
        for a in self.actions:
            # Précondition unaire
            if isinstance(a.precondition, Predicate):
                p = a.precondition
                names = [t.name.upper() for t in p.terms]
                predicat = f"{p.name}({','.join(names)})" if len(names) > 0 else f"{p.name}"
                params_names = [t.name.upper() for t in a.parameters]
                action = f"{a.name}({','.join(names)})" if len(params_names) > 0 else f"{a.name}"
                preconditions += f"pre({action}, {predicat}) :- action({action}).\n"
            # On ne traite pas les prédicats négatifs
            elif not isinstance(a.precondition, Not):
                for p in a.precondition.operands:
                    if isinstance(p, Not):
                        continue
                    names = [t.name.upper() for t in p.terms]
                    predicat = f"{p.name}({','.join(names)})" if len(names) > 0 else f"{p.name}"
                    params_names = [t.name.upper() for t in a.parameters]
                    action = f"{a.name}({','.join(params_names)})" if len(params_names) > 0 else f"{a.name}"
                    preconditions += f"pre({action}, {predicat}) :- action({action}).\n"
        # On s'assure qu'une action n'est réalisée que si ses préconditions sont vérifiées
        preconditions += "\n:- perform(A,T), pre(A,C), not holds(C,T), time(T).\n"
        return preconditions
    
    def write_positive_effects(self):
        # On écrit les effets positifs add(A,F)
        positive_effects = ""
        for a in self.actions:
            # Action avec un seul effet positif
            if isinstance(a.effect, Predicate):
                p = a.effect
                names = [t.name.upper() for t in p.terms]
                predicat = f"{p.name}({','.join(names)})" if len(names) > 0 else f"{p.name}"
                params_names = [t.name.upper() for t in a.parameters]
                action = f"{a.name}({','.join(params_names)})" if len(params_names) > 0 else f"{a.name}"
                positive_effects += f"add({action}, {predicat}) :- action({action}).\n"
            # Action avec plusieurs effets
            elif not isinstance(a.effect, Not):
                for p in a.effect.operands:
                    # On ignore les prédicats négatifs qui sont des effets négatifs
                    if isinstance(p, Not):
                        continue
                    names = [t.name.upper() for t in p.terms]
                    predicat = f"{p.name}({','.join(names)})" if len(names) > 0 else f"{p.name}"
                    params_names = [t.name.upper() for t in a.parameters]
                    action = f"{a.name}({','.join(params_names)})" if len(params_names) > 0 else f"{a.name}"
                    positive_effects += f"add({action}, {predicat}) :- action({action}).\n"
        # On ajoute le fluent F à l'étape T+1 si l'action A est réalisée à l'étape T
        positive_effects += "\nholds(F,T+1) :- perform(A,T), add(A,F).\n"
        return positive_effects

    def write_negative_effects(self):
        # On écrit les effets négatifs del(A,F)
        negative_effects = ""
        for a in self.actions:
            # Action avec un seul effet négatif
            if isinstance(a.effect, Not):
                p = a.effect.argument
                names = [t.name.upper() for t in p.terms]
                predicat = f"{p.name}({','.join(names)})" if len(names) > 0 else f"{p.name}"
                params_names = [t.name.upper() for t in a.parameters]
                action = f"{a.name}({','.join(params_names)})" if len(params_names) > 0 else f"{a.name}"
                negative_effects += f"del({action}, {predicat}) :- action({action}).\n"
            # Action avec plusieurs effets
            elif not isinstance(a.effect, Predicate):
                for p in a.effect.operands:
                    # On ignore les effets positifs
                    if isinstance(p, Predicate):
                        continue
                    p = p.argument
                    names = [t.name.upper() for t in p.terms]
                    predicat = f"{p.name}({','.join(names)})" if len(names) > 0 else f"{p.name}"
                    params_names = [t.name.upper() for t in a.parameters]
                    action = f"{a.name}({','.join(params_names)})" if len(params_names) > 0 else f"{a.name}"
                    negative_effects += f"del({action}, {predicat}) :- action({action}).\n"
        # On propage les fluents F à l'instant T+1 à moins que l'action A réalisée à l'instant T ne supprime F
        negative_effects += "\nholds(F,T+1) :- holds(F,T), perform(A,T), not del(A,F), time(T).\n"
        return negative_effects

    def write(self):
        lines = "% Declaration du domaine\n\n"
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
        # Objets utilisés dans le programme
        objects = ""
        for o in self.objects:
            objects += f"{o.type_tag}({o.name.lower()}).\n"
        return objects
    
    def write_init(self):
        init = ""
        for i in self.init:
            if isinstance(i, Predicate):
                names = [t.name.lower() for t in i.terms]
                predicat = f"{i.name}({','.join(names)})" if len(names) > 0 else f"{i.name}"
                init += f"init({predicat}).\n"
            # On ignore les prédicats négatifs
            elif isinstance(i, Not):
                continue
        # Les fluents initiaux sont vrais à l'instant 0
        init += "\nholds(F,0) :- init(F).\n"
        return init
    
    def write_goal(self):
        goal = ""
        # Un seul objectif
        if isinstance(self.goal, Predicate):
            names = [t.name.lower() for t in self.goal.terms]
            predicat = f"{self.goal.name}({','.join(names)})" if len(names) > 0 else f"{self.goal.name}"
            goal += f"but({predicat}).\n"

        # Plusieurs objectifs
        elif not isinstance(self.goal, Not):
            for g in self.goal.operands:
                if isinstance(g, Predicate):
                    names = [t.name.lower() for t in g.terms]
                    predicat = f"{g.name}({','.join(names)})" if len(names) > 0 else f"{g.name}"
                    goal += f"but({predicat}).\n"
                # On ignore les prédicats négatifs
                elif isinstance(g, Not):
                    continue
        # On s'assure que les fluents de l'objectif sont vrais à l'instant n
        goal += "\n:- but(F), not holds(F,n).\n"
        return goal

    def write(self):
        lines = "% Declaration du probleme\n\n"
        lines += "% Declaration des objets\n\n" + self.write_objects()
        lines += "\n\n% Etat initial\n\n" + self.write_init()
        lines += "\n\n% Specification du but\n\n" + self.write_goal()
        return lines



class PDDLWriter(object):
    def __init__(self, domain_name, problem_name):
        self.domain = DomainWriter(domain_name)
        self.problem = ProblemWriter(problem_name)

    def write(self, filename, n):
        with open(filename, "w") as f:
            f.write(f"#const n = {n}.\ntime(0..n).\n\n\n")
            f.write(self.domain.write())
            f.write("\n\n\n")
            f.write(self.problem.write())
            f.write("\n\n\n")
            f.write("% Choix d'action\n\n" + "1{perform(A,T): action(A)}1 :- time(T), time(T+1).\n")
            f.write("\n\n#show perform/2.\n")



if __name__ == "__main__":
    writer = PDDLWriter("./pddl_examples/blockWorld-domain.pddl", "./pddl_examples/blockWorld-problem.pddl")
    writer.write("./outputs/blockworld.lp", 10)