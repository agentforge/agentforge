import networkx as nx
from typing import Dict, List
from collections import defaultdict
from pddlpy import DomainProblem
from graphviz import Digraph
import re

# Function to convert a predicate dictionary into a string representation
def predicate_to_str(predicate):
    if isinstance(predicate, dict):
        return " ".join([" ".join([k] + predicate[k]) for k in predicate])
    return predicate

def add_preconditions(precond, action, G, dot, addtl_links, negate=False, previous_precond=None):
    if isinstance(precond, dict):
        for key, value in precond.items():
            if key == "and":
                for item in value:
                    add_preconditions(item, action, G, dot, addtl_links, negate=negate)
            elif key == "or":
                prev_or_precond = None
                for item in value:
                    prev_or_precond = add_preconditions(item, action, G, dot, addtl_links, negate=negate, previous_precond=prev_or_precond)
            elif key == "not":
                add_preconditions(value, action, G, dot, addtl_links, negate=True)
            else:
                precond_str = "not " + predicate_to_str(precond) if negate else predicate_to_str(precond)
                G.add_edge(precond_str, action, label="precondition")
                dot.edge(precond_str, action, color="blue")
                addtl_links[key] = precond
                if previous_precond:
                    G.add_edge(previous_precond, precond_str, label="OR")
                    dot.edge(previous_precond, precond_str, color="orange", label="OR")
                return precond_str
    else:
        precond_str = "not " + precond if negate else precond
        G.add_edge(precond_str, action, label="precondition")
        dot.edge(precond_str, action, color="blue")
        if previous_precond:
            G.add_edge(previous_precond, precond_str, label="OR")
            dot.edge(previous_precond, precond_str, color="orange", label="OR")
        return precond_str


def add_effects(effect, action, G, dot, negate=False):
    if isinstance(effect, dict):
        for key, value in effect.items():
            if key == "and":
                for item in value:
                    add_effects(item, action, G, dot, negate=negate)
            elif key == "not":
                add_effects(value, action, G, dot, negate=True)
            else:
                effect_str = "not " + predicate_to_str(effect) if negate else predicate_to_str(effect)
                G.add_edge(action, effect_str, label="effect")
                dot.edge(action, effect_str, color="red")
    else:
        effect_str = "not " + effect if negate else effect
        G.add_edge(action, effect_str, label="effect")
        dot.edge(action, effect_str, color="red")

def create_graph(parameter_types, actions, preconditions, effects):
    G = nx.DiGraph()
    dot = Digraph(strict=True)
    addtl_links = {}

    def add_node(graph, name, shape="ellipse", **kwargs):
        graphviz_attrs = {key: str(value) for key, value in kwargs.items()}
        graph.add_node(name, **kwargs)
        dot.node(name, shape=shape, **graphviz_attrs)

    def add_edge(graph, src, dst, color="black", label=""):
        graph.add_edge(src, dst, color=color, label=label)
        dot.edge(src, dst, color=color, label=label)

    # Function to extract types from action parameters
    def extract_types_from_parameters(parameter_types, parameters):
        for key, var_type in parameters.items():
            parameter_types[key] = var_type

    for action, detail in actions.items():
        extract_types_from_parameters(parameter_types, detail["parameters"])
        add_node(G, action, shape="box", parameters=detail["parameters"])

    for action, precond in preconditions.items():
        add_preconditions(precond, action, G, dot, addtl_links)

    # Additional links for effects
    for action, effect in effects.items():
        add_effects(effect, action, G, dot)

    # Additional links
    print(f"{addtl_links=}")
    print(f"{effects=}")
    for action, effect_list in effects.items():
        for effect_key, val in effect_list.items():
            valid1 = effect_key in addtl_links.keys()
            if not valid1:
                continue
            valid2 = val != addtl_links[effect_key][effect_key]
            # valid3 = "not " + effect != addtl_links[effect_list[0]]
            print(f"{valid1} and {valid2}")
            if valid1 and valid2:
                print(f"{effect_key=}")
                print(f"{addtl_links[effect_key]=}")
                add_edge(G, effect_key + " " + val[0], effect_key + " " + addtl_links[effect_key][effect_key][0], label="polymorphic")

    return G, dot

# Updated visualize_graph function with concise string conversion
def visualize_graph(dot: Digraph):
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

def parse_predicate(predicate_str):
    predicate_parts = [part.strip("()") for part in predicate_str.strip().split()]
    return {predicate_parts[0]: [p.strip("()") for p in predicate_parts[1:]]}

def split_bracketed_expressions(expr_str):
    expressions = []
    start = 0
    bracket_count = 0
    for i, char in enumerate(expr_str):
        if char == '(':
            bracket_count += 1
        elif char == ')':
            bracket_count -= 1
            if bracket_count == 0:
                expressions.append(expr_str[start:i+1])
                start = i+2
    return expressions

def parse_expression(expr_str):
    expr_str = expr_str.strip()
    if expr_str.startswith('(and'):
        return {'and': [parse_expression(e) for e in split_bracketed_expressions(expr_str[5:-1].strip())]}
    elif expr_str.startswith('(or'):
        return {'or': [parse_expression(e) for e in split_bracketed_expressions(expr_str[4:-1].strip())]}
    elif expr_str.startswith('(not'):
        return {'not': parse_expression(expr_str[5:-1].strip())}
    else:
        return parse_predicate(expr_str[1:-1])

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
            precondition_line = line.split(":precondition")[1].strip()
            preconditions_dict[action_name] = parse_expression(precondition_line)
            inside_action = False
            action_name = None

    return preconditions_dict

def parse_effect_expression(expr_str):
    expr_str = expr_str.strip()
    if expr_str.startswith('(and'):
        return {'and': [parse_effect_expression(e) for e in split_bracketed_expressions(expr_str[5:-1].strip())]}
    elif expr_str.startswith('(not'):
        return {'not': parse_effect_expression(expr_str[5:-1].strip())}
    else:
        return parse_predicate(expr_str[1:-1])

def split_bracketed_expressions(expr_str):
    expressions = []
    start = 0
    bracket_count = 0
    for i, char in enumerate(expr_str):
        if char == '(':
            bracket_count += 1
        elif char == ')':
            bracket_count -= 1
            if bracket_count == 0:
                expressions.append(expr_str[start:i+1])
                start = i+2
    return expressions

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
            effect_line = line.split(":effect")[1].strip()
            effects_dict[action_name] = parse_effect_expression(effect_line)
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


# Function to extract the last variable from a string or dictionary expression
def extract_last_variable_from_expression(expression):
    if isinstance(expression, dict):
        expression_str = " ".join([k] + expression[k] for k in expression)
    else:
        expression_str = expression
    pattern = r'\?[\w\-]+'
    matches = re.findall(pattern, expression_str)
    return matches[-1] if matches else None

# Updated function to run on a root node
def run_node(objects, node):
    variable = extract_last_variable_from_expression(node)
    if variable:
        objects[variable].add(node)

# Updated function to run on a root edge
def run_edge(objects, edges):
    for edge in edges:
        variable = extract_last_variable_from_expression(edge)
        if variable:
            objects[variable].add(edge)

# Updated function to evaluate a node
def eval_node(objects, graph, node):
    predecessors = list(graph.predecessors(node))
    if not predecessors:
        run_node(objects, node)
    return True

# Updated function to evaluate an edge
def eval_edge(objects, graph, edge):
    predecessors = list(graph.predecessors(edge[0]))
    if not predecessors:
        run_edge(objects, edge)
    return True

# Function to trace the PDDL graph (unchanged)
def trace_pddl_graph(objects, graph, root_node):
    visited_nodes = set()
    trace_graph(objects, graph, root_node, visited_nodes)
    # Convert the sets to lists before returning
    return {key: list(value) for key, value in objects.items()}

# Recursive function to trace the graph (unchanged)
def trace_graph(objects, graph, node, visited_nodes):
    if node in visited_nodes:
        return
    visited_nodes.add(node)
    eval_node(objects, graph, node)
    for predecessor in graph.predecessors(node):
        edge = (predecessor, node)
        eval_edge(objects, graph, edge)
        trace_graph(objects, graph, predecessor, visited_nodes)


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
    print("Actions:")
    for action_name, action_details in actions.items():
        print(f"  {action_name}: {action_details}")

    print("\n\nPredicates:")
    print(predicates)

    print("\n\nEffects:")
    print(effects)

    print("\n\nPreconditions:")
    print(preconditions)

    print("\n\nTypes:")
    print(types)

    G, dot = create_graph(parameter_types, actions, preconditions, effects)
    visualize_graph(dot)

    # Trace the graph starting from "growing ?seedling"
    objects = trace_pddl_graph(objects, G, seed)
    final_objs = {}
    for k,v in objects.items():
        parameter_type = parameter_types[k]
        type_ = lookup_type(type_klasses, types, parameter_type)
        final_objs[k] = {"class": parameter_type, "predicates": v, "type": f"{type_}"}
        if parameter_type in types:
            final_objs[k]["parent"] = types[parameter_type]

    return final_objs
