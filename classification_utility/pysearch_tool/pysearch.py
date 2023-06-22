# import git
#import subprocess
#(might delete if never used) import pathlib
import os
import ast
from lxml import etree,html
import xml.etree.ElementTree as ET

class pysearch:
    def __init__(self, methods_path, app_path, prob_path):
        """
        search earch repository in given path, extract the
        first line.

        Parameters
        ----------------
        method_path : str
            the folder that contains inference methods in CoFI
        app_path : str
            the folder that contains applications in espresso
        prob_path : str
            the folder that contains example problems in CoFI
            examples
        """
        self._method_path = methods_path
        self._app_path = app_path
        self._prob_path = prob_path
        self._methods = []
        self._apps = []
        self._problems = []

    def mds(self):
        return self._methods
    
    def aps(self):
        return self._apps

    def search(self, ignore):
        # methods = []  # Store the found methods
        # apps = []  # Store the found apps

        # Inference methods in CoFI
        for root, _, files in os.walk(self._method_path):
            for method in files:
                if method.endswith("-checkpoint.py"):
                    continue  # Skip temporary checkpoint files
                if method not in ignore:
                    method_path = os.path.join(root, method)
                    with open(method_path) as file:
                        lines = file.readlines()

                    method_name = ""
                    method_tree = []
                    description = ""

                    for line in lines:
                        line = line.strip()
                        if line.startswith("# Method : "):
                            method_name = line[11:]
                        elif line.startswith("# CoFI"):
                            method_tree = line[10:].strip().split(" -> ")
                        elif line.startswith("# description:"):
                            description = line[15:]
                    print(method_name)
                    print(method_tree)
                    print(description)
                    self._methods.append(Method(method_name, method_path, method_tree, description))
        # Inference applications in CoFI
        for root, dirs, files in os.walk(self._app_path):
            if root == self._app_path:
                for dirr in dirs:
                    if dirr not in ignore:
                        app_path = self._app_path + '/' + dirr + '/' + dirr + '.py'
                        r = open(app_path)
                        if os.path.exists(app_path):
                            app_name = r.readline().strip('\n')[2:]
                            app_tree = r.readline().strip('\n')[2:].split(" -> ")
                            app_des = r.readline().strip('\n')[15:]
                            self._apps.append(App(app_name, app_path, app_tree, app_des))
                            print(app_tree)
    
    def _search(self):

        def parse(file_path):
            res = []
            with open(file_path) as file:
                while True:
                    line = file.readline()
                    if line:
                        if line[0:11] == "# Method : ":
                            method_name = line.strip('\n')[11:]
                            method_tree = file.readline().strip('\n')[2:].split(" -> ")
                            method_description = file.readline().strip('\n')[15:]
                            method = Method(method_name, file_path, method_tree, method_description)
                            self._methods.append(method)
                        if line[0:16] == "# Application : ":
                            app_name = line.strip('\n')[16:]
                            app_tree = file.readline().strip('\n')[2:].split(" -> ")
                            app_des = file.readline().strip('\n')[15:]
                            self._apps.append(App(app_name, file_path, app_tree, app_des))                    
                    else:
                        break


        for _, _ , files in os.walk(self._method_path):
            for i in files:
                parse(self._method_path + '/' + i)

        for root, dirs, files in os.walk(self._app_path):
            if root == self._app_path:
                for dirr in dirs:
                    parse(self._app_path + '/' + dirr + '/' + dirr + '.py')

    def search_examples(self, ignore):
        for root, _, files in os.walk(self._prob_path):
            for file_name in files:
                if file_name.endswith(".py"):
                    if file_name not in ignore:
                        file_path = os.path.join(root, file_name)
                        description = self.parse_description(file_path)
                        self._problems.append(Example(file_name, file_path, description))

    def parse_description(self, file_path):
        with open(file_path) as file:
            content = file.read()

        tree = ast.parse(content)
        docstrings = ast.get_docstring(tree)
        return docstrings if docstrings else ""

    def problems(self):
        return self._problems
        
class Method:
    def __init__(self, name, path, tree, des):
        """
        A single Method defination.

        Parameters
        -----------
        name : str
            method name
        path : str
            method file path
        tree : list
            tree path of the method
        """
        self._name = name
        self._path = path
        self._tree = tree
        self._des = des
    
    def name(self):
        return self._name
    
    def path(self):
        return self._path
    
    def tree(self):
        return self._tree
    
    def des(self):
        return self._des
    
class App:
    def __init__(self, name, path, tree, des):
        """
        A single Method defination.

        Parameters
        -----------
        name : str
            method name
        path : str
            method file path
        tree : list
            tree path of the method
        """
        self._name = name
        self._path = path
        self._tree = tree
        self._des = des
    
    def name(self):
        return self._name
    
    def path(self):
        return self._path
    
    def tree(self):
        return self._tree
    
    def des(self):
        return self._des
            

class Example:
    def __init__(self, name, path, description):
        self._name = name
        self._path = path
        self._description = description
    
    def name(self):
        return self._name
    
    def path(self):
        return self._path
    
    def description(self):
        return self._description

    
class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []
        
    def add_child(self, child):
        self.children.append(child)
        
    def is_leaf(self):
        return len(self.children) == 0        


def find_leaf_nodes(tree):
    if tree.is_leaf():
        return [tree.name]
    leaf_nodes = []
    for child in tree.children:
        leaf_nodes.extend(find_leaf_nodes(child))
    return leaf_nodes


def build_tree():
    root = TreeNode("CoFI - Common Framework for Inference")

    param_estimation = TreeNode("Parameter estimation")
    root.add_child(param_estimation)

    matrix_based_solvers = TreeNode("Matrix based solvers")
    param_estimation.add_child(matrix_based_solvers)

    linear_system_solvers = TreeNode("Linear system solvers")
    matrix_based_solvers.add_child(linear_system_solvers)

    optimization = TreeNode("Optimization")
    param_estimation.add_child(optimization)

    non_linear = TreeNode("Non linear")
    optimization.add_child(non_linear)

    linear = TreeNode("Linear")
    optimization.add_child(linear)

    ensemble_methods = TreeNode("Ensemble methods")
    root.add_child(ensemble_methods)

    direct_search = TreeNode("Direct Search")
    ensemble_methods.add_child(direct_search)

    monte_carlo = TreeNode("Monte Carlo")
    direct_search.add_child(monte_carlo)

    deterministic = TreeNode("Deterministic")
    direct_search.add_child(deterministic)

    bayesian_sampling = TreeNode("Bayesian Sampling")
    ensemble_methods.add_child(bayesian_sampling)

    mcmc_samplers = TreeNode("McMC samplers")
    bayesian_sampling.add_child(mcmc_samplers)

    trans_d_mcmc = TreeNode("Trans-D McMC")
    bayesian_sampling.add_child(trans_d_mcmc)

    return root


def print_tree(node, indent=""):
    if type(node.name) == tuple:
        example = node.name
        print(indent + " - Name: {}".format(example[0]))
        print(indent + " - Path: {}".format(example[1]))
        print(indent + " - Description: {}".format(example[2]))
        print()
        print()
    else:
        print(indent + node.name)
    for child in node.children:
        print_tree(child, indent + "  ")
        

def map_examples_to_leaf_nodes(node, mappings):
    if node.name in mappings:
        examples = mappings[node.name]
        node.children = [TreeNode((example[0], example[1], example[2])) for example in examples]
    else:
        for child in node.children:
            map_examples_to_leaf_nodes(child, mappings)
            
            
    
if __name__ == "__main__": 
    methods_path = "cofi/src/cofi/tools"
    applications_path = "espresso/contrib"
    problems_path = "cofi-examples/examples"
    ignore_list = ['__init__.py', '_base_inference_tool.py']

    p = pysearch(methods_path, applications_path, problems_path)
    p._search()
    p.search_examples(ignore_list)
    problems = p.problems()
    

    # Build the tree
    root_node = build_tree()

    # Print the tree
    #print_tree(root_node)
    
   
    # for problem in problems:
    #     print("Name:", problem.name())
    #     print("Path:", problem.path())
    #     print("Description:", problem.description())
    #     print()
    
    # Find the leaf nodes
    leaf_nodes = find_leaf_nodes(root_node)

    # # Print the leaf nodes
    # for leaf_node in leaf_nodes:
    #     print(leaf_node)



    mappings = {leaf_node: [] for leaf_node in leaf_nodes}

    for example in problems:
        description = example.description()
        if "linear system solver" in description.lower():
            mappings["Linear system solvers"].append((example.name(), example.path(), example.description()))
        elif "non-linear" in description.lower():
            mappings["Non linear"].append((example.name(), example.path(), example.description()))
        elif "linear" in description.lower():
            mappings["Linear"].append((example.name(), example.path(), example.description()))
        elif "monte carlo" in description.lower():
            mappings["Monte Carlo"].append((example.name(), example.path(), example.description()))
        elif "deterministic" in description.lower():
            mappings["Deterministic"].append((example.name(), example.path(), example.description()))
        elif "emcee" in description.lower():
            mappings["McMC samplers"].append((example.name(), example.path(), example.description()))
        elif "trans-d" in description.lower():
            mappings["Trans-D McMC"].append((example.name(), example.path(), example.description()))



    # Map the examples to the leaf nodes
    map_examples_to_leaf_nodes(root_node, mappings)

    # Print the updated tree structure
    print_tree(root_node)