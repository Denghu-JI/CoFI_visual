# import git
#import subprocess
#(might delete if never used) import pathlib
import os
import ast
from config import methods_path, applications_path, problems_path, ignore_list

def is_legal_node_name(node, level, legal_node_names):
    # Check if the node is in the legal node names for the given level
    if level in legal_node_names:
        return node in legal_node_names[level]
    
    return False

def load_legal_names():
    legal_node_names = {}

    # Read the legal node names from the file
    with open("legal_node_names.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line:
                level, names = line.split(":")
                level = int(level)
                names = [name.strip() for name in names.split(",")]
                legal_node_names[level] = names
    
    return legal_node_names

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
        self._legal_names = load_legal_names()

    def mds(self):
        return self._methods
    
    def aps(self):
        return self._apps
    
    
    def _search(self):
              

        def parse(file_path):
            
            def print_illegal_node_names(illegal_nodes):
                if illegal_nodes:
                    print(f"Illegal node name(s) encountered in {file_path}:")
                    for level, node_name in illegal_nodes:
                        print(f"Level {level}: {node_name}")
                        
            res = []
            line_number = 0
            with open(file_path) as file:
                while True:
                    line_number += 1
                    line = file.readline()
                    if line:
                        if line[0:11] == "# Method : ":
                            method_name = line.strip('\n')[11:]
                            method_tree = file.readline().strip('\n')[2:].split(" -> ")
                            method_description = file.readline().strip('\n')[15:]
                            illegal_nodes = [(i + 1, node) for i, node in enumerate(method_tree) if not is_legal_node_name(node, i + 1, self._legal_names)]
                            if illegal_nodes:
                                print_illegal_node_names(illegal_nodes)
                                raise ValueError(f"Illegal node name(s) encountered in method_tree at line {line_number} in file {file_path}")
                            method = Method(method_name, file_path, method_tree, method_description)   
                            self._methods.append(method)
                        if line[0:16] == "# Application : ":
                            app_name = line.strip('\n')[16:]
                            app_tree = file.readline().strip('\n')[2:].split(" -> ")
                            app_des = file.readline().strip('\n')[15:]
                            self._apps.append(App(app_name, file_path, app_tree, app_des))
                    else:
                        break


        for _, _, files in os.walk(self._method_path):
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
        self._tree_path = ""

    def name(self):
        return self._name

    def path(self):
        return self._path

    def description(self):
        return self._description

    def tree_path(self):
        return self._tree_path

    def set_tree_path(self, tree_path):
        self._tree_path = tree_path


    
class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.examples = []
        self.parent = None

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

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

def add_examples_to_tree(root_node, example_objects, current_path=""):
    for example in example_objects:
        description = example.description().lower()  # Convert to lowercase
        added = False

        for node in root_node.traverse():
            node_name_lower = node.name.lower()
            if node_name_lower in description or node_name_lower + 's' in description:
                # Construct the tree path by including the root node at the start
                path_to_example = root_node.name + " -> " + current_path + " -> " + example.name()
                example.set_tree_path(path_to_example)

                # Add the example to the node
                node.add_example(example)

                added = True
                break  # Exit the inner loop after finding a match

        if not added:
            # If no matching node is found, add the example to the root node
            path_to_example = root_node.name + " -> " + example.name()
            example.set_tree_path(path_to_example)
            root_node.add_example(example)

    for child in root_node.children:
        add_examples_to_tree(child, example_objects, current_path=root_node.name)

    return root_node



def get_example_tree_paths(root_node):
    example_paths = []

    def traverse(node, current_path=""):
        if node.examples:
            for example in node.examples:
                example_path = current_path + " -> " + example.name()
                example_paths.append((example.name(), example.path(), example.description(), example_path))

        for child in node.children:
            traverse(child, current_path=current_path + " -> " + child.name)

    traverse(root_node)
    return example_paths

def print_tree(root_node, indent=''):
    print(f"{indent}{root_node.name}")
    for child in root_node.children:
        print_tree(child, indent + '  ')
    if root_node.examples:
        for example in root_node.examples:
            print(f"{indent}  Example: {example.name()} ({example.path()})")
            print(f"{indent}    Description: {example.description()}")

            
    
if __name__ == "__main__":
    tree_lists = []

    p = pysearch(methods_path, applications_path, problems_path)
    p._search()
    p.search_examples(ignore_list)
    problems = p.problems()

    for method in p._methods:
        tree_lists.append(method.tree())

    root_node = build_tree_from_lists(tree_lists)
    root_node = add_examples_to_tree(root_node, problems)
    
    example_paths = get_example_tree_paths(root_node)
    for example_path in example_paths:
        print("Example Tree Path:", example_path[3])
        print()

    print_tree(root_node)