import os
import networkx as nx
from typing import Dict, List, Any
from collections import defaultdict
from pddlpy import DomainProblem
from pddlpy.pddl import Atom
from graphviz import Digraph
import re, json
from agentforge.utils import logger
from agentforge.interfaces import interface_interactor
from datetime import datetime

from pydantic import BaseModel, Field
from typing import List, Optional, Dict

"""
Core functionality:

get_seed_queries(goal) -> List[Dict[str, Any]]:

* Extracts the PDDL dependency graph from the given domain
creates a visualisation of the graph

* Backtracks through the graph to find the root nodes and edges

* Generates queries to the user based on the unknown root nodes and
edges. The prompts are generated based on the preconditions and effects
using the LLM.


Then once necessary information is gathered we use PDDL to 
create the problem PDDL file from PDDLFragments so that 
the Plan can be executed
"""

# TODO: Add a function to serialize/deserialize planning graphs to/from JSON
# TODO: Simplify to use a cached version of the graphs
# TODO: Alter eval node/edge functions to query knowledge base

def set_to_list(s):
    if len(s) == 0:
        return []
    
    serialized_list = []
    for item in s:
        if isinstance(item, Atom):
            serialized_list.append(str(item))
        else:
            serialized_list.append(item)
            
    return serialized_list

class PDDLFragment(BaseModel):
    type: Optional[str] = Field(None)
    objects: Optional[List[str]] = Field(None)
    instances: Optional[List[str]] = Field(None)
    predicate: Optional[str] = Field(None)

    """
        Input - PDDLFragment

        Output - (type, fragment)
            
        Given the goal, object, and predicate we can create a PDDL problem fragment
        These values are optional and can be None. If they are None we do not
        return that fragment.

        A predicate can have multiple objects, i.e. "has-seed-type ?seed ?plant"

        Example:
            {
                "val": "(growing ?plant)",
                "type": "goal"
            }
    
    """
    def init_pddl_problem_fragment(self) -> List[dict]:
        inst = [i.replace(" ", "-") for i in self.instances]
        if self.type == "goal":
            return [{
                "val":f"({self.predicate} {' '.join(inst)})",
                "type": "goal"
            }]
        elif self.type == "init":
            return [{
                "val":f"({self.predicate} {' '.join(inst)})",
                "type": "init"
            }]
        elif self.type == "object":
            vals = zip(self.objects, inst)
            return [{
                "val":f"{instance} - {obj.replace(' ', '-')}",
                "type": "object"
            } for obj, instance in vals]

class PDDLGraphModel(BaseModel):
    domain_file: Optional[str] = ""
    problem_file: Optional[str] = ""
    id: Optional[str] = ""
    parameter_types: Optional[Dict[str, Any]] = Field(default=None)
    types: Optional[Dict[str, Any]] = Field(default=None)
    attributes: Optional[Dict[str, Any]] = Field(default=None)
    effects: Optional[Dict[str, Any]] = Field(default=None)
    actions: Optional[Dict[str, Any]] = Field(default=None)
    predicates: Optional[Dict[str, Any]] = Field(default=None)
    preconditions: Optional[Dict[str, Any]] = Field(default=None)
    created_dt: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_dt: Optional[datetime] = Field(default=None)

class PDDLGraph:
    def __init__(self, domain_file: str, problem_file: str, primary_key: str):
        self.db = interface_interactor.get_interface("db")

        # Dynamically initialize attributes based on the Pydantic model
        for field in PDDLGraphModel.__annotations__.keys():
            setattr(self, field, None if field != "types" else {})

        # Override defaults
        self.id = primary_key
        self.domain_file = domain_file
        self.problem_file = problem_file

        self.deserialize_from_db()

    def deserialize_from_db(self) -> None:
        # Fetch the data from MongoDB based on the primary key
        db_data = self.db.get("pddl", self.id)
        
        if db_data:
            # Use Pydantic for deserialization
            pddl_graph_model = PDDLGraphModel(**db_data)
            
            # Populate  the object variables dynamically
            for field, value in pddl_graph_model.dict().items():
                setattr(self, field, value)

    def serialize_to_json_and_db(self) -> None:
        # Initialize an empty Pydantic model
        pddl_graph_model = PDDLGraphModel()

        # Dynamically populate the Pydantic model with data from the PDDLGraph object
        for field in PDDLGraphModel.__annotations__.keys():
            value = getattr(self, field, None)
            setattr(pddl_graph_model, field, value)

        # Serialize using the Pydantic model
        serialized_data = pddl_graph_model.dict()

        # Check if an entry with the same primary key already exists
        existing_entry = self.db.get("pddl", self.id)

        if existing_entry:
            # Update the existing entry
            self.db.set("pddl", self.id, serialized_data)
        else:
            # Create a new entry
            self.db.create("pddl", self.id, serialized_data)

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

    def generate_all_prompts(self, preconditions):
        prompts = defaultdict(list)
        # logger.info("generate_all_prompts")
        for action_name, precondition in preconditions.items():
            # logger.info(f"{action_name=}")
            queries = self.process_precondition(precondition)
            # logger.info(f"{len(queries)}")
            # logger.info(f"{queries}")
            for query in queries:
                prompts[action_name].append(query)
        return prompts

    # Function to convert a predicate dictionary into a string representation
    def predicate_to_str(self, predicate):
        if isinstance(predicate, dict):
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
                        G.add_edge(precond_str, previous_precond, label="OR")
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

        # Function to extract types from action parameters
        def extract_types_from_parameters(parameters):
            for key, var_type in parameters.items():
                self.parameter_types[key] = var_type

        for action, detail in actions.items():
            extract_types_from_parameters(detail["parameters"])
            add_node(G, action, shape="box", parameters=detail["parameters"], label=action)

        for action, precond in preconditions.items():
            # logger.info(f"[PRECOND] {precond}")
            self.add_preconditions(precond, action, G, dot)

        # Additional links for effects
        for action, effect in effects.items():
            self.add_effects(effect, action, G, dot)

        # logger.info(G.nodes(data=True))  # Attributes of all nodes
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
            # logger.info("PARSE_EXPRESSION")
            # logger.info(expr_str)
            val = self.parse_predicate(expr_str[1:-1])
            # logger.info(val)
            return val

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

    # get the predicate of the 'predicate ?object' string
    # for negated elemnts ignore the 'not' and get the predicate
    def root_element(self, node):
        eles = node.split(" ")
        if eles[0] != "not":
            return eles[0]
        return eles[1] # negation

    # Function to extract the last variable from a string or dictionary expression
    def extract_last_variable_from_expression(self, expression):
        # logger.info("[EXTRACTING] " + expression)
        if expression in self.attributes:
            return self.attributes[expression]
        else:
            raise ValueError("FAIL")
        if isinstance(expression, dict):
            expression_str = " ".join([k] + expression[k] for k in expression)
        else:
            expression_str = expression
        pattern = r'\?[\w\-]+'
        matches = re.findall(pattern, expression_str)
        return matches[-1] if matches else None

    def has_edge_with_label(self, node, label='OR'):
        for neighbor in self.G.neighbors(node):
            if 'label' in self.G[node][neighbor] and self.G[node][neighbor]['label'] == label:
                return True, neighbor  # Returns True and the neighbor connected by this edge
        return False, None  # Returns False if no such edge exists


    # Updated function to run on a root node
    def run_node(self, objects, node):
        print(f"RUNING {node}")
        action = [i for i in self.G.successors(node)]
        # logger.info(f"{node=}")
        # logger.info(f"{action=}")
        variables = self.extract_last_variable_from_expression(node)
        for variable in variables:
            if node not in objects[variable]:
                objects[variable].append(node)

    # Updated function to run on a root edge
    def run_edge(self, objects, edge):
        print(f"RUNING EDGE {edge}")
        # logger.info(f"[EDGE] {edge}")
        action = [i for i in self.G.successors(self.root_element(edge))]
        # logger.info(f"EDGE ACTION: {action}")
        valid_actions = [a for a in action if a in self.actions]
        variables = self.extract_last_variable_from_expression(edge)
        for variable in variables:
            for splitvar in variable.split(" "):
                objects[splitvar] = list(set(objects[splitvar]).union(set(valid_actions)))

    # if this node has been evaluated -- action
    def is_evaluated_node(self, node):
        print("EVAL NODE")
        is_action = node in self.actions
        is_predicate = node in self.predicates
        if is_predicate:
            return self.eval_predicate(node)
        print(f"{node}: Action? {is_action} Pred? {is_predicate}")
        # check knowledge base for node
        return False

    # if this edge -- precondition or effect
    def is_evaluated_edge(self, edge):
        print("EVAL EDGE")
        is_action = edge in self.actions
        is_predicate = edge in self.predicates
        if is_predicate:
            return self.eval_predicate(edge)
        print(f"{edge}: Action? {is_action} Pred? {is_predicate}")
        # check knowledge base for node
        return False

    def eval_predicate(self, predicate):
        print(f"EVAL PREDICATE {len(list(self.G.predecessors(self.root_element(predicate))))}")
        print(predicate)
        print(self.G.nodes[predicate])
        # If there are no predecessors or all predecessors are already evaluated
        if len(list(self.G.predecessors(self.root_element(predicate)))) == 0:
            return True
        # check knowledge base for node
        return False

    # Updated function to evaluate a node 
    def eval_node(self, objects, node):
        predecessors = list(self.G.predecessors(self.root_element(node)))
        predecessors_evaled = [p for p in predecessors if not self.is_evaluated_node(p)]
        # If no predessors or all predessors are already evaluated
        print(node)
        print(predecessors_evaled)
        if not predecessors_evaled:
            self.run_node(objects, node)
            return False
        return True

    # Updated function to evaluate an edge
    def eval_edge(self, objects, edges):
        for edge in edges:
            predecessors = list(self.G.predecessors(self.root_element(edge)))
            predecessors_evaled = [p for p in predecessors if not self.is_evaluated_edge(p)]
            # If no predessors or all predessors are already evaluated
            if not predecessors_evaled:
                self.run_edge(objects, edge)
            return True

    # Function to trace the PDDL graph (unchanged)
    def trace_pddl_graph(self, objects, root_node):
        visited_nodes = set()
        print("objects bevore trace")
        print(objects)
        self.trace_graph(objects, root_node, visited_nodes)
        print("objects after trace")
        print(json.dumps(objects, indent=4))
        for obj, action_list in objects.items():
            print(obj.split(" "))
        # Convert the sets to lists before returning
        return {key: list(value) for key, value in objects.items()}

    # Recursive function to trace the graph (unchanged)
    def trace_graph(self, objects, node, visited_nodes):
        if node in visited_nodes:
            return
        visited_nodes.add(node)
        cont = self.eval_node(objects, node)
        if not cont:
            return
        for predecessor in self.G.predecessors(self.root_element(node)):
            edge = (predecessor, node)
            self.eval_edge(objects, edge)
            self.trace_graph(objects, predecessor, visited_nodes)

    # Lookup type for this objeect, drilling down if necessary
    def lookup_type(self, type_klasses: List, types: Dict, key: str) -> str:
        if key in types and types[key] in type_klasses:
            return types[key]
        elif key in types and types[key] in types:
            return self.lookup_type(type_klasses, types, types[key])

    """
        Iterates the entire graph and creates necessary state but does not traverse
        the graph to find the root nodes/edges
    """
    def setup_graph(self):
        # For production environments use the pre-loaded graph state
        dev = os.getenv("ENV") == "dev" or os.getenv("ENV") == "test"
        # if self.updated_dt is not None and not dev:
        #     return

        # Dictionary to keep track of variable types
        self.parameter_types = {}
        self.type_klasses = ["boolean", "object", "numeric", "string", "array", "null"]

        # Dictionary to keep track of objects and their corresponding unique root nodes/edges
        self.objects = defaultdict(list)

        # Extracting the information from the PDDL 2.1 files
        domprob = DomainProblem(self.domain_file, self.problem_file)

        self.worldobjects = domprob.worldobjects()
        print(self.worldobjects)
        # Extracting all actions (operators)
        self.actions = {}
        # print(domprob.ground_operator('prepare'))
        for operator_name in domprob.operators():
            operator = domprob.domain.operators[operator_name]
            print(operator)
            self.actions[operator_name] = {
                "parameters": operator.variable_list,
                "positive_preconditions": set_to_list(operator.precondition_pos),
                "negative_preconditions": set_to_list(operator.precondition_neg),
                "positive_effects": set_to_list(operator.effect_pos),
                "negative_effects": set_to_list(operator.effect_neg),
                # You can extract additional attributes of the operator here
            }

        # Extracting all predicates (this may require additional parsing logic based on the PDDL structure)
        self.predicates = self.extract_predicates(self.domain_file)

        # You may add additional extraction logic for other elements of the PDDL files here
        self.effects = self.extract_effects(self.domain_file)

        self.preconditions = self.extract_preconditions(self.domain_file)

        # Test the further adjusted extract_types function with the given PDDL file
        self.types = self.extract_types(self.domain_file)

        # Printing the extracted information
        # print("Actions:")
        # for action_name, action_details in self.actions.items():
        #     print(f"  {action_name}: {action_details}")

        # print("\n\nPredicates:")
        # print(predicates)

        # print("\n\nEffects:")
        # print(effects)

        # print("\n\nPreconditions:")
        # print(json.dumps(self.preconditions, indent=2))

        # logger.info("\n\nTypes:")
        # logger.info(json.dumps(self.types))

        self.G, self.dot = self.create_graph(self.actions, self.preconditions, self.effects)
        attributes = nx.get_edge_attributes(self.G, 'variables')
        self.attributes = defaultdict(list)
        for k,v in attributes.items():
            for item in k:
                self.attributes[item].append(v)

        # logger.info("ATTRIBUTES...")
        # logger.info(self.attributes)
        self.visualize_graph(self.dot)
        self.updated_dt = datetime.utcnow()
        self.serialize_to_json_and_db()

    """
        Input seed: str
        Given a seed goal, identify nodes at the edge of the graph where we
        do not have information and need to query the environment or the user

    """

    def get_seed_queries(self, seed: str):
        # setup graph if needed
        self.setup_graph()

        # Trace the graph starting from "growing ?seedling"
        objects = self.trace_pddl_graph(self.objects, seed)
        
        # logger.info(f"{objects=}")
        # logger.info(len(objects))
        # prompts = generate_all_prompts(actions, predicates, effects, preconditions)
        final_queries = {}

        # Generate the prompts
        prompts = self.generate_all_prompts(self.preconditions)
        print("PROMPTPS FOR SEEDDDD")
        print(json.dumps(prompts, indent=4))

        # Print the prompts for the "prepare" action as examples
        # for prompt in prompts["prepare"]:
        #     print(prompt)

        print("parameter_types")
        print(self.parameter_types)

        final_queries = defaultdict(list)
        # For each object/action list generate queries
        for obj, action_list in objects.items():
            # for each action -- referenced by the object

            for action in action_list:
                # if we have already evaled this action or it is not in the prompts
                if not (action and action in prompts):
                    continue

                for prompt in prompts[action]:
                    print(prompt.split(" ")[-1])

                    # ignore root negation preconditions for now, and make sure the obj/prompt pair is valid
                    if prompt[0:4] == "not " or obj not in prompt:
                        continue

                    # also ignore OR singletons, should be capture by OR boolean prompt
                    print(prompt.split(" ")[0])
                    or_cond, node = self.has_edge_with_label(prompt.split(" ")[0])
                    if or_cond and " OR " not in prompt:
                        continue

                    parameter_type = self.parameter_types[prompt.split(" ")[-1]]
                    type_ = self.lookup_type(self.type_klasses, self.types, parameter_type)
                    query = {'condition': prompt, "datatype": type_, "class": parameter_type}
                    final_queries[action].append(query)

        return final_queries

class PDDL:
    def __init__(self, pddl_graph):
        self.pddl_graph = pddl_graph
    
    """
        Executes the actions in the plan iteratively updating the state
    """
    def execute_plan(self, plan):
        pass

    """
    # We need to iterate through the responses and create the PDDL problem
    """
    def create_pddl_problem_state(self, queries: List[Dict], goal: str) -> List[Dict]:
        self.variables = defaultdict(list)

        # Add all queried objects and init states
        fragments = []
        for query in queries:
            # logger.info(query)

            # BOOLEAN CASE
            if query['datatype'] == "boolean" and len(query["results"]) > 0:
                # If the response is true create a init and object fragment
                if query["results"][0] == True:
                    predicate = list(query["predicates"].keys())[0]
                    instances = [i.replace("?", "") for i in query["predicates"][predicate]] # replace ?
                    fragments.append(PDDLFragment(type="object", objects=[query["class"]], instances=instances))
                    fragments.append(PDDLFragment(type="init", predicate=predicate, instances=instances))
                # If the response is false create object fragment
                if query["results"][0] == False:
                    fragments.append(PDDLFragment(type="object", objects=[query["class"]], instances=[query["class"]]))

            # STRING CASE
            elif query['datatype'] == "string":
                objs = [query["class"] for i in range(len(query["results"]))]

                # maintain a list of obj/type pairings for our goal
                for obj, result in zip(objs, query["results"]):
                    self.variables[obj].append(result)

                for result in query["results"]:
                    predicate = result.replace(" ", "-")
                    if predicate in query["predicates"]: #if the predicate is the result, this is an OR BRANCH
                        instances = [i.replace("?", "") for i in query["predicates"][predicate]] # replace ?
                    else: # This is a root String Node, i.e. no branching we need to capture the sematnic info
                        predicate = list(query["predicates"].keys())[0]
                        instances = [result]

                    init_fragment = PDDLFragment(type="init", predicate=predicate, instances=instances)
                    object_fragment = PDDLFragment(type="object", objects=objs, instances=instances)
                    fragments.append(init_fragment)
                    fragments.append(object_fragment)

            ## IF THIS IS A SUBTYPE WE SHOULD SAVE THAT INFORMATION SOMEWHERE
            if query["class"] in self.pddl_graph.types and self.pddl_graph.types[query["class"]] != query['datatype']:
                pass

        # Add all objects to the problem
        for _, obj_type in self.pddl_graph.parameter_types.items():
            fragments.append(PDDLFragment(type="object", objects=[obj_type], instances=[obj_type]))

        # LAST add the goal statement
        # logger.info(f"{self.variables=}")
        goal_data = goal.split(" ")
        objs = goal_data[1:]
        goal = goal_data[0]
        instances = []
        for obj in objs:
            clean_obj = self.pddl_graph.parameter_types[obj]
            instances.append(clean_obj)
            # instances.extend(self.variables[clean_type])

        obj = obj.replace("?", "") # TODO: add support for multi-predicate goals
        goal_arr = [PDDLFragment(type="goal", instances=instances, predicate=goal)]
        return [i.init_pddl_problem_fragment() for i in fragments + goal_arr]

def test():
    domain_file = '/app/agentforge/agentforge/config/planner/garden/domain.pddl'
    problem_file = '/app/agentforge/agentforge/config/planner/garden/problem.pddl'
    pddl_graph = PDDLGraph(domain_file, problem_file, "garden")
    pddl = PDDL(pddl_graph)
    queries = pddl_graph.get_seed_queries("growing ?cannabis-plant")
    print(json.dumps(queries))
    return pddl_graph
