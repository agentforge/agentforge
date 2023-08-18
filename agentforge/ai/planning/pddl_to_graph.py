import networkx as nx
from typing import Dict, List
from collections import defaultdict
from pddlpy import DomainProblem
from graphviz import Digraph
import re

# Function to extract types from action parameters
def extract_types_from_parameters(parameter_types, parameters):
    # print(f"{parameters=}")
    for key, var_type in parameters.items():
        parameter_types[key] = var_type

# Function to create the graph
def create_graph(parameter_types, actions, preconditions, effects):
    G = nx.DiGraph()
    addtl_links = {}

    # Add actions as nodes
    for action, detail in actions.items():
        extract_types_from_parameters(parameter_types, detail["parameters"])
        G.add_node(action, parameters=detail["parameters"])

    # Add edges for preconditions and effects
    for action, precond_list in preconditions.items():
        for precond in precond_list:
            precond_list = precond.split(" ")
            idx = 0
            while precond_list[idx] in ["not", "(", "and", "or"]:
                idx += 1
            addtl_links[precond_list[idx]] = precond
            G.add_edge(precond, action, label="precondition")
    
    for action, effect_list in effects.items():
        for effect in effect_list:
            G.add_edge(action, effect, label="effect")

    # Additional links
    for action, effect_list in effects.items():
        for effect in effect_list:
            effect_list = effect.split(" ")
            valid1 = effect_list[0] in addtl_links.keys()
            if not valid1:
                continue
            valid2 = effect != addtl_links[effect_list[0]]
            valid3 = "not " + effect != addtl_links[effect_list[0]]
            if valid1 and valid2 and valid3:
                G.add_edge(effect, addtl_links[effect_list[0]], label="additional_link")

    return G

# Definition of the function to create the graph
def create_viz_graph(actions, preconditions, effects):
    graph = {}
    for action, details in actions.items():      
        graph[action] = {
            "preconditions": preconditions.get(action, []),
            "effects": effects.get(action, []),
            "parameters": details["parameters"]
        }
    return graph

# Defining the visualize_graph function as provided earlier
def visualize_graph(graph):
    addtl_links = {}
    dot = Digraph(strict=True)
    for action, connections in graph.items():
        dot.node(action, shape="box", style="filled", color="lightyellow")
        for precond in connections['preconditions']:
            # for effect to precond matching
            precond_list = precond.split(" ")
            idx = 0
            while precond_list[idx] in ["not", "(", "and", "or"]:
                idx += 1
            addtl_links[precond_list[idx]] = precond
            dot.node(precond, shape="ellipse", style="filled", color="lightblue")
            dot.edge(precond, action, color="blue")
        for effect in connections['effects']:
            dot.node(effect, shape="ellipse", style="filled", color="lightgreen")
            dot.edge(action, effect, color="red")

    # additonal links
    for action, connections in graph.items():
        for effect in connections['effects']:
            effect_list = effect.split(" ")
            valid1 = effect_list[0] in addtl_links.keys()
            if not valid1:
                continue
            valid2 = effect != addtl_links[effect_list[0]]
            valid3 = "not " + effect != addtl_links[effect_list[0]]
            if valid1 and valid2 and valid3 :
                dot.edge(effect, addtl_links[effect_list[0]], color="green")

    # Render the graph and save it
    dot.render('./garden_graph', format='png', cleanup=True)
    return dot

# Further adjustment to correctly handle types without a subtype
def extract_types(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    types_dict = {}
    inside_types = False

    for line in lines:
        line = line.strip()

        if line.startswith("(:types"):
            inside_types = True
            continue

        if inside_types and line.endswith(")"):
            inside_types = False
            continue

        if inside_types:
            if " - " in line:
                subtypes, main_type = line.split(" - ")
                subtypes_list = subtypes.split()
                for subtype in subtypes_list:
                    types_dict[subtype] = main_type
            else:
                for individual_type in line.split():
                    types_dict[individual_type] = []

    return types_dict

# Definition of the function to extract preconditions from a PDDL file
def extract_preconditions(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    preconditions_dict = {}
    inside_action = False
    action_name = None

    for line in lines:
        line = line.strip()

        if line.startswith("(:action"):
            inside_action = True
            action_name = line.split()[1]

        if inside_action and line.startswith(":precondition"):
            preconditions_list = []
            precondition_line = line.split(":precondition")[1].strip()
            if precondition_line.startswith("(and"):
                preconditions = precondition_line[5:-1].split(') (')
                for precondition in preconditions:
                    preconditions_list.append(precondition.strip().replace("(", "").replace(")", ""))
            else:
                preconditions_list.append(precondition_line.strip().replace("(", "").replace(")", ""))

            preconditions_dict[action_name] = preconditions_list
            inside_action = False
            action_name = None

    return preconditions_dict

# Definition of the function to extract effects from a PDDL file
def extract_effects(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    effects_dict = {}
    inside_action = False
    action_name = None

    for line in lines:
        line = line.strip()

        if line.startswith("(:action"):
            inside_action = True
            action_name = line.split()[1]

        if inside_action and line.startswith(":effect"):
            effects_list = []
            effect_line = line.split(":effect")[1].strip()
            if effect_line.startswith("(and"):
                effects = effect_line[5:-1].split(') (')
                for effect in effects:
                    effects_list.append(effect.strip().replace("(", "").replace(")", ""))
            else:
                effects_list.append(effect_line.strip().replace("(", "").replace(")", ""))

            effects_dict[action_name] = effects_list
            inside_action = False
            action_name = None

    return effects_dict

def extract_predicates(file_name: str) -> Dict[str, str]:
    predicates = {}
    
    # Read the content of the file
    with open(file_name, 'r') as file:
        content = file.read()
    
    # Extract the section containing predicates
    predicates_section_start = content.find("(:predicates") + len("(:predicates")
    predicates_section_end = predicates_section_start
    open_paren_count = 1

    # Find the matching closing parenthesis for the predicates section
    while open_paren_count > 0 and predicates_section_end < len(content):
        char = content[predicates_section_end]
        if char == '(':
            open_paren_count += 1
        elif char == ')':
            open_paren_count -= 1
        predicates_section_end += 1

    predicates_section = content[predicates_section_start:predicates_section_end - 1].strip()

    # Split the section into lines and extract the predicates and their parameters
    current_predicate = ""
    for char in predicates_section:
        if char == '(':
            current_predicate = char
        elif char == ')':
            current_predicate += char
            predicate_parts = current_predicate[1:-1].split(' ', 1)
            predicates[predicate_parts[0]] = predicate_parts[1]
            current_predicate = ""
        else:
            current_predicate += char
            
    return predicates

def extract_pddl_info(domain_file, problem_file):
    # Initialize the DomainProblem with the given domain and problem files
    domprob = DomainProblem(domain_file, problem_file)

    # Extracting all actions (operators)
    actions = {}
    for operator_name in domprob.operators():
        operator = domprob.domain.operators[operator_name]
        actions[operator_name] = {
            "parameters": operator.variable_list,
            # You can extract additional attributes of the operator here
        }

    # Extracting all predicates (this may require additional parsing logic based on the PDDL structure)
    predicates = extract_predicates(domain_file)

    # You may add additional extraction logic for other elements of the PDDL files here
    effects = extract_effects(domain_file)

    preconditions = extract_preconditions(domain_file)

    # Test the further adjusted extract_types function with the given PDDL file
    types = extract_types(domain_file)


    return actions, predicates, effects, preconditions, types

def extract_last_variable_from_string(string):
    pattern = r'\?[\w\-]+'
    matches = re.findall(pattern, string)
    return matches[-1] if matches else None

# Function to run on a root node
def run_node(objects, node):
    variable = extract_last_variable_from_string(node)
    if variable:
        objects[variable].add(node)

# Function to run on a root edge
def run_edge(objects, edges):
    for edge in edges:
        variable = extract_last_variable_from_string(edge)
        if variable:
            objects[variable].add(edge)

# Function to evaluate a node
def eval_node(objects, graph, node):
    predecessors = list(graph.predecessors(node))
    # print(f"{predecessors=}, {node=}")
    if not predecessors:
        run_node(objects, node)
    return True

# Function to evaluate an edge
def eval_edge(objects, graph, edge):
    predecessors = list(graph.predecessors(edge[0]))
    # print(f"{predecessors=}, {edge=}")
    if not predecessors:
        run_edge(objects, edge)
    return True

# Recursive function to trace the graph
def trace_graph(objects, graph, node, visited_nodes):
    if node in visited_nodes:
        return
    visited_nodes.add(node)
    eval_node(objects, graph, node)
    for predecessor in graph.predecessors(node):
        edge = (predecessor, node)
        eval_edge(objects, graph, edge)
        trace_graph(objects, graph, predecessor, visited_nodes)

# Function to trace the PDDL graph
def trace_pddl_graph(objects, graph, root_node):
    visited_nodes = set()
    trace_graph(objects, graph, root_node, visited_nodes)
    # Convert the sets to lists before returning
    return {key: list(value) for key, value in objects.items()}

# Lookup type for this objeect, drilling down if necessary
def lookup_type(type_klasses: List, types: Dict, key: str) -> str:
    if key in types and types[key] in type_klasses:
        return types[key]
    elif key in types and types[key] in types:
        return lookup_type(type_klasses, types, types[key])

def get_seed_queries(seed: str, domain_file: str, problem_file: str):
    # Dictionary to keep track of variable types
    parameter_types = {}
    type_klasses = ["boolean", "object", "numeric", "string", "array", "null"]

    # Dictionary to keep track of objects and their corresponding unique root nodes/edges
    objects = defaultdict(set)

    # Extracting the information from the PDDL 2.1 files
    actions, predicates, effects, preconditions, types = extract_pddl_info(domain_file, problem_file)

    # Printing the extracted information
    # print("Actions:")
    # for action_name, action_details in actions.items():
    #     print(f"  {action_name}: {action_details}")

    # print("\n\nPredicates:")
    # print(predicates)

    # print("\n\nEffects:")
    # print(effects)

    # print("\n\nPreconditions:")
    # print(preconditions)

    # print("\n\nTypes:")
    # print(types)

    G = create_graph(parameter_types, actions, preconditions, effects)

    # Visualization for debugging
    # GV = create_viz_graph(actions, preconditions, effects)
    # visualize_graph(GV)

    # Trace the graph starting from "growing ?seedling"
    objects = trace_pddl_graph(objects, G, seed)
    final_objs = {}
    for k,v in objects.items():
        parameter_type = parameter_types[k]
        type_ = lookup_type(type_klasses, types, parameter_type)
        final_objs[k] = {"class": parameter_type, "predicates": v, "type": f"{type_}"}
        if parameter_type in types:
            final_objs[k]["parent"] = types[parameter_type]

    print(f"{final_objs=}")
    return final_objs
