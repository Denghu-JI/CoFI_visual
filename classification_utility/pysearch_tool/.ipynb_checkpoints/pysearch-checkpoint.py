# import git
#import subprocess
#(might delete if never used) import pathlib
import os

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
        self.examples = []

        
    def add_child(self, child):
        self.children.append(child)

    def add_example(self, example):
        self.examples.append(example)

    def traverse(self):
        yield self
        for child in self.children:
            yield from child.traverse()       


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
        

def add_examples_to_tree(root_node, example_objects):
    for example in example_objects:
        description = example.description()
        for node in root_node.traverse():
            if node.name in description:
                node.add_example(example)
    return root_node
            
def build_tree_from_lists(tree_lists):
    root = None
    node_dict = {}

    for tree_list in tree_lists:
        parent_name = tree_list[0]

        if parent_name not in node_dict:
            parent_node = TreeNode(parent_name)
            node_dict[parent_name] = parent_node

            if root is None:
                root = parent_node
        else:
            parent_node = node_dict[parent_name]

        for node_name in tree_list[1:]:
            if node_name not in node_dict:
                node = TreeNode(node_name)
                node_dict[node_name] = node
            else:
                node = node_dict[node_name]

            # Check if the node already exists as a child
            existing_child = next((child for child in parent_node.children if child.name == node_name), None)
            if existing_child:
                parent_node = existing_child
            else:
                parent_node.add_child(node)
                parent_node = node

    return root


def add_examples_to_tree(root_node, example_objects):
    for example in example_objects:
        description = example.description().lower()  # Convert to lowercase
        for node in root_node.traverse():
            node_name_lower = node.name.lower()
            if node_name_lower in description or node_name_lower + 's' in description:
                node.add_example(example)
                break  # Exit the inner loop after finding a match
    return root_node


def print_tree(root_node, indent=''):
    print(f"{indent}{root_node.name}")
    for child in root_node.children:
        print_tree(child, indent + '  ')
    if root_node.examples:
        for example in root_node.examples:
            print(f"{indent}  Example: {example.name()} ({example.path()})")
            print(f"{indent}    Description: {example.description()}")

            
    
if __name__ == "__main__": 
    methods_path = "cofi/src/cofi/tools"
    applications_path = "espresso/contrib"
    problems_path = "cofi-examples/examples"
    ignore_list = ['__init__.py', '_base_inference_tool.py']
    tree_lists = []

    p = pysearch(methods_path, applications_path, problems_path)
    p._search()
    p.search_examples(ignore_list)
    problems = p.problems()
    
    
    for method in p._methods:
        tree_lists.append(method.tree())

    root_node = build_tree_from_lists(tree_lists)
    add_examples_to_tree(root_node, problems)
    print_tree(root_node)
    