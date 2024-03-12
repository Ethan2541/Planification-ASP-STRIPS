from PDDLWriter import PDDLWriter
import datetime
import os
import sys

def find_minimal_plan(domain_file, problem_file):
    current_datetime = datetime.datetime.now()
    timestamp = current_datetime.timestamp()
    dir_name = f"./outputs/output_{timestamp}"
    os.mkdir(dir_name)

    for n in range(1, 1000):
        asp_filename = f"{dir_name}/asp.lp"
        results_filename = f"{dir_name}/results_{n}.lp"
        writer = PDDLWriter(domain_file, problem_file)
        writer.write(asp_filename, n)

        os.system("clingo " + domain_file + " " + f" > {results_filename}")
        with open(results_filename) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        for line in content:
            if line.startswith("Answer"):
                return line
    return "No plan found"
    

if __name__ == "__main__":
    domain_file, problem_file = sys.argv[1], sys.argv[2]
    find_minimal_plan(domain_file, problem_file)