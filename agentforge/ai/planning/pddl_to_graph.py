import networkx as nx
from typing import Dict, List
from collections import defaultdict
from pddlpy import DomainProblem
from graphviz import Digraph
import re, json
from agentforge.utils import logger


class QueryGenerator:
    def __init__(self):
        pass

    def loads(self, actions, predicates, effects):
        self.actions = actions
        self.predicates = predicates
        self.effects = effects

    def process_precondition(self, precondition):
        queries = []
        and_conditions = precondition.get("and", [])
        for condition in and_conditions:
            if "or" in condition:
                or_conditions = condition["or"]
                or_query = " OR ".join([f"{key} {value[0] if isinstance(value, list) else value}" for item in or_conditions for key, value in item.items()])
                queries.append(or_query)
            else:
                for key, value in condition.items():
                    value_str = value[0] if isinstance(value, list) else value
                    queries.append(f"{key} {value_str}")
        return queries

    def generate_precondition_prompt(self, action_name, precond_str):
        prompt_context = f"""
        You are an AI assistant aware of various tasks and their requirements. Here are the details of the tasks and conditions:

        Actions:
        {self.actions[action_name]}

        Predicates:
        {self.predicates}

        Precondition for '{action_name}':
        {precond_str}

        Effects:
        {self.effects[action_name]}

        You need to inquire about the requirements for the action '{action_name}'. Frame a question that encompasses the relationships in the precondition.
        """
        return prompt_context

    def generate_all_prompts(self, preconditions):
        prompts = defaultdict(list)
        logger.info("generate_all_prompts")
        for action_name, precondition in preconditions.items():
            logger.info(f"{action_name=}")
            queries = self.process_precondition(precondition)
            logger.info(f"{len(queries)}")
            logger.info(f"{queries}")
            for query in queries:
                # prompt = self.generate_precondition_prompt(action_name, query)
                prompts[action_name].append(query)
        return prompts

    # Function to convert a predicate dictionary into a string representation
    def predicate_to_str(self, predicate):
        if isinstance(predicate, dict):
            if len(predicate.keys()) > 1:
                logger.info("RED ALERT!!!!! ")
            # return predicate.keys()[0]
            predicate_str = " ".join([" ".join([k]) for k in predicate])
            vars = " ".join([" ".join(predicate[k]) for k in predicate])
        return predicate_str, vars

    def add_preconditions(self, precond, action, G, dot, negate=False, previous_precond=None):
        if isinstance(precond, dict):
            for key, value in precond.items():
                if key == "and":
                    for item in value:
                        self.add_preconditions(item, action, G, dot, negate=negate)
                elif key == "or":
                    prev_or_precond = None
                    for item in value:
                        prev_or_precond = self.add_preconditions(item, action, G, dot, negate=negate, previous_precond=prev_or_precond)
                elif key == "not":
                    self.add_preconditions(value, action, G, dot, negate=True)
                else:
                    precond, variables = self.predicate_to_str(precond)
                    precond_str = "not " + precond if negate else precond
                    G.add_edge(precond_str, action, label="precondition", variables=variables)
                    dot.edge(precond_str, action, color="blue")
                    # addtl_links[key] = precond
                    if previous_precond:
                        G.add_edge(previous_precond, precond_str, label="OR")
                        dot.edge(previous_precond, precond_str, color="orange", label="OR")
                    return precond_str
        else:
            precond, variables = self.predicate_to_str(precond)
            precond_str = "not " + precond if negate else precond
            G.add_edge(precond_str, action, label="precondition", variables=variables)
            dot.edge(precond_str, action, color="blue")
            if previous_precond:
                G.add_edge(previous_precond, precond_str, label="OR")
                dot.edge(previous_precond, precond_str, color="orange", label="OR")
            return precond_str


    def add_effects(self, effect, action, G, dot, negate=False):
        if isinstance(effect, dict):
            for key, value in effect.items():
                if key == "and":
                    for item in value:
                        self.add_effects(item, action, G, dot, negate=negate)
                elif key == "not":
                    self.add_effects(value, action, G, dot, negate=True)
                else:
                    effect, variables = self.predicate_to_str(effect)
                    effect_str = "not " + effect if negate else effect
                    G.add_edge(action, effect_str, label="effect", variables=variables)
                    dot.edge(action, effect_str, color="red")
        else:
            effect, variables = self.predicate_to_str(effect)
            effect_str = "not " + effect if negate else effect
            G.add_edge(action, effect_str, label="effect", variables=variables)
            dot.edge(action, effect_str, color="red")

    def create_graph(self, actions, preconditions, effects):
        G = nx.DiGraph()
        dot = Digraph(strict=True)

        def add_node(graph, name, shape="ellipse", **kwargs):
            graphviz_attrs = {key: str(value) for key, value in kwargs.items()}
            graph.add_node(name, **kwargs)
            dot.node(name, shape=shape, **graphviz_attrs)

        def add_edge(graph, src, dst, color="black", label=""):
            graph.add_edge(src, dst, color=color, label=label)
            dot.edge(src, dst, color=color, label=label)

        # Function to extract types from action parameters
        def extract_types_from_parameters(parameters):
            for key, var_type in parameters.items():
                self.parameter_types[key] = var_type

        for action, detail in actions.items():
            extract_types_from_parameters(detail["parameters"])
            add_node(G, action, shape="box", parameters=detail["parameters"], label=action)

        for action, precond in preconditions.items():
            logger.info(f"[PRECOND] {precond}")
            self.add_preconditions(precond, action, G, dot)

        # Additional links for effects
        for action, effect in effects.items():
            self.add_effects(effect, action, G, dot)

        # Additional links
        # for action, effect_list in effects.items():
        #     for effect_key, val in effect_list.items():
        #         valid1 = effect_key in addtl_links.keys()
        #         if not valid1:
        #             continue
        #         valid2 = val != addtl_links[effect_key][effect_key]
        #         if valid1 and valid2:
        #             add_edge(G, effect_key + " " + val[0], effect_key + " " + addtl_links[effect_key][effect_key][0], label="polymorphic")
        logger.info(G.nodes(data=True))  # Attributes of all nodes
        return G, dot

    # Updated visualize_graph function with concise string conversion
    def visualize_graph(self, dot: Digraph):
        dot.render('./garden_graph', format='png', cleanup=True)
        return dot

    # Further adjustment to correctly handle types without a subtype
    def extract_types(self, file_name):
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

    def parse_predicate(self, predicate_str):
        predicate_parts = [part.strip("()") for part in predicate_str.strip().split()]
        return {predicate_parts[0]: [p.strip("()") for p in predicate_parts[1:]]}

    def split_bracketed_expressions(self, expr_str):
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

    def parse_expression(self, expr_str):
        expr_str = expr_str.strip()
        if expr_str.startswith('(and'):
            return {'and': [self.parse_expression(e) for e in self.split_bracketed_expressions(expr_str[5:-1].strip())]}
        elif expr_str.startswith('(or'):
            return {'or': [self.parse_expression(e) for e in self.split_bracketed_expressions(expr_str[4:-1].strip())]}
        elif expr_str.startswith('(not'):
            return {'not': self.parse_expression(expr_str[5:-1].strip())}
        else:
            return self.parse_predicate(expr_str[1:-1])

    def extract_preconditions(self, file_name):
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
                preconditions_dict[action_name] = self.parse_expression(precondition_line)
                inside_action = False
                action_name = None

        return preconditions_dict

    def parse_effect_expression(self, expr_str):
        expr_str = expr_str.strip()
        if expr_str.startswith('(and'):
            return {'and': [self.parse_effect_expression(e) for e in self.split_bracketed_expressions(expr_str[5:-1].strip())]}
        elif expr_str.startswith('(not'):
            return {'not': self.parse_effect_expression(expr_str[5:-1].strip())}
        else:
            return self.parse_predicate(expr_str[1:-1])

    def split_bracketed_expressions(self, expr_str):
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

    def extract_effects(self, file_name):
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
                effects_dict[action_name] = self.parse_effect_expression(effect_line)
                inside_action = False
                action_name = None

        return effects_dict

    def extract_predicates(self, file_name: str) -> Dict[str, str]:
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

    def extract_pddl_info(self, domain_file, problem_file):
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
        predicates = self.extract_predicates(domain_file)

        # You may add additional extraction logic for other elements of the PDDL files here
        effects = self.extract_effects(domain_file)

        preconditions = self.extract_preconditions(domain_file)

        # Test the further adjusted extract_types function with the given PDDL file
        types = self.extract_types(domain_file)


        return actions, predicates, effects, preconditions, types

    # get the predicate of the 'predicate ?object' string
    # for negated elemnts ignore the 'not' and get the predicate
    def root_element(self, node):
        eles = node.split(" ")
        if eles[0] != "not":
            return eles[0]
        return eles[1] # negation

    # Function to extract the last variable from a string or dictionary expression
    def extract_last_variable_from_expression(self, expression):
        logger.info("[EXTRACTING] " + expression)
        if isinstance(expression, dict):
            expression_str = " ".join([k] + expression[k] for k in expression)
        else:
            expression_str = expression
        pattern = r'\?[\w\-]+'
        matches = re.findall(pattern, expression_str)
        return matches[-1] if matches else None

    # Updated function to run on a root node
    def run_node(self, objects, graph, node):
        action = [i for i in graph.successors(node)]
        logger.info(f"{node=}")
        logger.info(f"{action=}")
        variable = self.extract_last_variable_from_expression(node)
        if variable:
            if len(action[0].split(" ")) > 1:
                key = "edge"
            else:
                key = "action"
            objects[variable].append({key: action, "variable": variable})

    # Updated function to run on a root edge
    def run_edge(self, objects, graph, edges):
        for edge in edges:
            logger.info(f"[EDGE] {edge}")
            action = [i for i in graph.successors(self.root_element(edge))]
            logger.info(f"EDGE ACTION: {action}")
            variable = self.extract_last_variable_from_expression(edge)
            if variable:
                print(variable)
                if len(action[0].split(" ")) > 1:
                    objects[variable].append({"predicate": action[0]})
                else:
                    objects[variable].append({"action": action[0]})
        else:
                print("NO EDGE?", edge)

    # Updated function to evaluate a node
    def eval_node(self, objects, graph, node):
        predecessors = list(graph.predecessors(self.root_element(node)))
        if not predecessors:
            self.run_node(objects, graph, node)
        return True

    # Updated function to evaluate an edge
    def eval_edge(self, objects, graph, edge):
        predecessors = list(graph.predecessors(self.root_element(edge[0])))
        if not predecessors:
            self.run_edge(objects, graph, edge)
        return True

    # Function to trace the PDDL graph (unchanged)
    def trace_pddl_graph(self, objects, graph, root_node):
        visited_nodes = set()
        self.trace_graph(objects, graph, root_node, visited_nodes)
        # Convert the sets to lists before returning
        return {key: list(value) for key, value in objects.items()}

    # Recursive function to trace the graph (unchanged)
    def trace_graph(self, objects, graph, node, visited_nodes):
        if node in visited_nodes:
            return
        visited_nodes.add(node)
        self.eval_node(objects, graph, node)
        for predecessor in graph.predecessors(self.root_element(node)):
            edge = (predecessor, node)
            self.eval_edge(objects, graph, edge)
            self.trace_graph(objects, graph, predecessor, visited_nodes)


    # Lookup type for this objeect, drilling down if necessary
    def lookup_type(self, type_klasses: List, types: Dict, key: str) -> str:
        if key in types and types[key] in type_klasses:
            return types[key]
        elif key in types and types[key] in types:
            return self.lookup_type(type_klasses, types, types[key])

    def get_seed_queries(self, seed: str, domain_file: str, problem_file: str):
        # Dictionary to keep track of variable types
        self.parameter_types = {}
        type_klasses = ["boolean", "object", "numeric", "string", "array", "null"]

        # Dictionary to keep track of objects and their corresponding unique root nodes/edges
        objects = defaultdict(list)

        query_generator = QueryGenerator()

        # Extracting the information from the PDDL 2.1 files
        actions, predicates, effects, preconditions, types = self.extract_pddl_info(domain_file, problem_file)

        query_generator.loads(actions, predicates, effects)

        # Printing the extracted information
        print("Actions:")
        for action_name, action_details in actions.items():
            print(f"  {action_name}: {action_details}")

        # print("\n\nPredicates:")
        # print(predicates)

        # print("\n\nEffects:")
        # print(effects)

        print("\n\nPreconditions:")
        logger.info(json.dumps(preconditions))

        # print("\n\nTypes:")
        logger.info(json.dumps(types))

        G, dot = self.create_graph(actions, preconditions, effects)
        self.visualize_graph(dot)

        # Trace the graph starting from "growing ?seedling"
        self.objects_store = {}
        objects = self.trace_pddl_graph(objects, G, seed)
        
        logger.info(objects)
        logger.info(len(objects))
        # prompts = generate_all_prompts(actions, predicates, effects, preconditions)
        final_queries = {}

        # Generate the prompts
        prompts = query_generator.generate_all_prompts(preconditions)
        logger.info(prompts)

        # Print the prompts for the "prepare" action as examples
        for prompt in prompts["prepare"]:
            print(prompt)

        raise ValueError("STOP")
        final_prompts = defaultdict(list)
        for obj, action_list in objects.items():
            parameter_type = self.parameter_types[obj]
            type_ = self.lookup_type(type_klasses, types, parameter_type)
            for action in action_list:
                if "predicate" in action:
                    action_name = action["predicate"]
                else:
                    action_name = action["action"]
                if action_name in prompts:
                    if action_name not in final_prompts:
                        final_prompts[action_name].append({'text': prompts[action_name], "type": type_, "class": parameter_type})

        # print(len(prompts)
        logger.info("FINAL PROMPTS")
        logger.info(len(final_prompts))
        return final_prompts

        # final_objs = {}
        # for k,v in objects.items():
        #     final_objs[k] = {"class": parameter_type, "predicates": v, "type": f"{type_}"}
        #     if parameter_type in types:
        #         final_objs[k]["parent"] = types[parameter_type]


    # Function to generate prompt for a specific precondition
    # def generate_precondition_prompt(actions, predicates, effects, action_name, precond_str):
    #     prompt_context = f"""
    #     You are an AI assistant aware of various tasks and their requirements. Here are the details of the tasks and conditions:

    #     Actions:
    #     {actions[action_name]}

    #     Predicates:
    #     {predicates}

    #     Precondition for '{action_name}':
    #     {precond_str}

    #     Effects:
    #     {effects[action_name]}

    #     You need to inquire about the requirements for the action '{action_name}'. Frame a question that encompasses the relationships in the precondition.
    #     """
    #     return prompt_context

    # def process_precondition(key, value, precond_str, parent=None):
    #     if key == "and":
    #         precond_str += " AND ".join([str(v) for v in value])
    #     elif key == "or":
    #         precond_str += " OR ".join([str(v) for v in value])
    #     elif key == "not":
    #         precond_str += " NOT " + str(value)
    #     else:
    #         precond_str += str(value)
    #     return precond_str

    # # Function to generate all prompts for the given preconditions
    # def generate_all_prompts(actions, predicates, effects, preconditions):
    #     prompts = defaultdict(list)
    #     for action_name, precond in preconditions.items():
    #         for key, value in precond.items():
    #             precond_str = process_precondition(key, value, "")
    #             p = generate_precondition_prompt(actions, predicates, effects, action_name, precond_str)
    #             prompts[action_name].append(p)
    #     return prompts

