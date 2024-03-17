from PDDLWriter import PDDLWriter
import datetime
import os
import sys
import time

max_n = 1000
path_clingo = "clingo"

def find_minimal_plan(domain_file, problem_file):
    # Timestamp pour le dossier de sortie
    current_datetime = datetime.datetime.now()
    timestamp = current_datetime.timestamp()
    dir_name = f"./outputs/output_{timestamp}"
    os.mkdir(dir_name)

    temps_initial = time.time()
    # Recherche itérative du plan minimal
    for n in range(1, max_n+1):
        asp_filename = f"{dir_name}/asp.lp"
        results_filename = f"{dir_name}/results_{n}.lp"
        # Traduction PDDL vers ASP-STRIPS
        writer = PDDLWriter(domain_file, problem_file)
        writer.write(asp_filename, n)

        # Résolution ASP
        os.system(f"{path_clingo} {asp_filename} > {results_filename}")
        with open(results_filename) as f:
            lines = f.readlines()
        lines = [line.strip() for line in lines]
        # On vérifie si c'est satisfiable
        for i, line in enumerate(lines):
            if line.startswith("Answer"):
                temps_final = time.time()
                print(f"Temps de calcul : {(temps_final - temps_initial):.2f} seconde(s)")
                return parse_answer(lines[i+1])
    print(f"Temps de calcul : {(temps_final - temps_initial):.2f} seconde(s)")
    return None

def parse_answer(answer):
    answer = answer.split(" ")
    plan = {}
    for a in answer:
        a = a[:-1].replace("perform(", "")
        time = int(a.split(",")[-1])
        action = ",".join(a.split(",")[0:-1])
        plan[time] = action
    return dict(sorted(plan.items()))
    

if __name__ == "__main__":
    domain_file, problem_file = sys.argv[1], sys.argv[2]
    plan = find_minimal_plan(domain_file, problem_file)
    if plan is not None:
        print(f"Longueur du plan minimal : n = {len(plan)} étapes")
        print("Plan minimal :")
        print("\n".join(["{: <8}".format(k) + v for k, v in plan.items()]))
    else:
        print(f"Pas de plan minimal pour n <= {max_n}")