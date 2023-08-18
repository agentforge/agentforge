import glob
import os
import sys
from collections import namedtuple


def find_build(fd_path):
    for release in ['release', 'release64', 'release32']:
        path = os.path.join(fd_path, 'builds/{}/'.format(release))
        if os.path.exists(path):
            return path
    raise RuntimeError('Please compile FastDownward first [.../pddlstream$ ./downward/build.py]')


directory = os.path.dirname(os.path.abspath(__file__))
FD_PATH = os.path.join(directory, '../../../downward')
TRANSLATE_PATH = os.path.join(find_build(FD_PATH), 'bin/translate')
sys.path.append(TRANSLATE_PATH)

from pddl_parser import pddl_file

Domain = namedtuple('Domain', ['name', 'requirements', 'types', 'type_dict', 'constants',
                               'predicates', 'predicate_dict', 'functions', 'actions', 'axioms'])
Problem = namedtuple('Problem', ['task_name', 'task_domain_name', 'task_requirements',
                                 'objects', 'init', 'goal', 'use_metric'])

domain_file = "domain.pddl"  # domain file for garden domain
problem_path = os.path.join(directory, 'g*.pddl')  # matching garden problem files
problem_files = glob.glob(problem_path)

for problem_file in problem_files:

    task = pddl_file.open(domain_file, problem_file)
    description = "Welcome to the garden! \n"
    
    # Iterate through the initial state and collect information
    for atom in task.init:
        if "plot-dug" == atom.predicate:
            description += f"The plot {atom.args[0]} is dug. \n"
        if "plot-fertilized" == atom.predicate:
            description += f"The plot {atom.args[0]} is fertilized. \n"
        if "plant-in" == atom.predicate:
            description += f"The plant {atom.args[0]} is in {atom.args[1]}. \n"
        if "plant-watered" == atom.predicate:
            description += f"The plant {atom.args[0]} is watered. \n"
        if "plant-matured" == atom.predicate:
            description += f"The plant {atom.args[0]} is matured. \n"
        if "tool-available" == atom.predicate:
            description += f"The tool {atom.args[0]} is available. \n"
        if "seed-available" == atom.predicate:
            description += f"The seed {atom.args[0]} is available. \n"
        if "container-available" == atom.predicate:
            description += f"The container {atom.args[0]} is available. \n"

    # Describe the goals
    description += "Your goal in this garden is: \n"
    if len(task.goal.parts) > 0:
        goals = task.goal.parts
    else:
        goals = [task.goal]
        
    for goal in goals:
        if goal.predicate == "plant-matured":
            description += f"The plant {goal.args[0]} should be matured. \n"
        elif goal.predicate == "plant-in":
            description += f"The plant {goal.args[0]} should be in {goal.args[1]}. \n"
        # Add other possible goal predicates here

    # Writing the description to a natural language file (.nl)
    nl_file = os.path.splitext(problem_file)[0] + ".nl"
    with open(nl_file, 'w') as f:
        f.write(description)

print("Natural language files have been generated.")
