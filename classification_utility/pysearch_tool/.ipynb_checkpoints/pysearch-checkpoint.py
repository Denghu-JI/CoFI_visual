import os
import yaml
from config import methods_path, applications_path, problems_path, ignore_list, valid_name
import re


method_headfix = "https://github.com/inlab-geo/cofi/blob/main"

application_headfix = "https://github.com/inlab-geo/espresso/tree/main"
folder_name = "contrib"


example_headfix = "https://github.com/inlab-geo/cofi-examples/tree/main/examples"


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
                names = [name.strip().lower() for name in names.split(",")]
                legal_node_names[level] = names
    
    return legal_node_names


def load_legal_anzsrc_names():
    legal_anzsrc_names = {}

    # Read the legal node names from the file
    with open("anzsrc.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line:
                level, names = line.split(":")
                level = int(level)
                names = [name.strip().lower() for name in names.split(",")]
                legal_anzsrc_names[level] = names
    
    return legal_anzsrc_names 

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
        self._examples = []
        self._legal_names = load_legal_names()
        self._legal_anzsrc_names = load_legal_anzsrc_names()

    def mds(self):
        return self._methods
    
    def aps(self):
        return self._apps

    def examples(self):
        return self._examples

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
                            
                            
   


    
    def _search(self):
        
        # def _is_legal_anzsrc(node_name, parent, level, legal_anzsrc_names):
        #     if level == 1:
        #         return node_name in legal_anzsrc_names
        #     else:
        #         parent_code = int(parent.split()[0])  # Extract the code from the parent node
        #         return (
        #         parent_code in legal_anzsrc_names and
        #         node_name in legal_anzsrc_names[parent_code]
        #         )

        def parse(file_path):
            res = []
            line_number = 0
            with open(file_path) as file:
                while True:
                    line = file.readline()
                    if line:
                        if line[0:11] == "# Method : ":
                            method_name = line.strip('\n')[11:]
                            method_tree = file.readline().strip('\n')[2:].split(" -> ")
                            method_description = file.readline().strip('\n')[15:]
                            illegal_nodes = [(i + 1, node) for i, node in enumerate(method_tree) if not is_legal_node_name(node.lower(), i + 1, self._legal_names)]
                            if illegal_nodes:
                                #print_illegal_node_names(illegal_nodes)
                                raise ValueError(f"Illegal node name(s) encountered in method_tree at line {line_number} in file {file_path}")
                            method = Method(method_name, method_headfix + file_path[18:], method_tree, method_description)
                            self._methods.append(method)
                        if line[0:16] == "# Application : ":
                            app_name = line.strip('\n')[16:]
                            app_tree = file.readline().strip('\n')[2:].split(" -> ")
                            app_des = file.readline().strip('\n')[15:]
                            app_path = application_headfix + file_path[22:]
                            
                            illegal_anzsrc = [(i + 1, node) for i, node in enumerate(app_tree) if not is_legal_node_name(node.lower(), i + 1, self._legal_anzsrc_names)]
                            if illegal_anzsrc:
                                print(f"Illegal anzsrc name(s): {illegal_anzsrc}")
                                raise ValueError(f"Illegal anzsrc name(s) encountered in method_tree at line {line_number} in file {file_path}")
                            self._apps.append(App(app_name, app_path, app_tree, app_des))
                    else:
                        break
                        


        for _, _ , files in os.walk(self._method_path):
            for i in files:
                parse(self._method_path + '/' + i)

        for root, dirs, files in os.walk(self._app_path):
            if root == self._app_path:
                for dirr in dirs:
                    parse(self._app_path + '/' + dirr + '/' + dirr + '.py')
        
        for root, dirs, files in os.walk(self._prob_path):
            if root == self._prob_path:
                for dirr in dirs:
                    try:
                        path = self._prob_path + '/' + dirr + '/'
                        with open(path + 'meta.yml', 'r') as file:
                            data = yaml.safe_load(file)
                            for i in range(len(data['notebook'][0]['file_to_parse'])):
                                if data['notebook'][0]['file_to_parse'][i] is not None:
                                    file_path = os.path.join(path, data['notebook'][0]['file_to_parse'][i])
                                    file_path = file_path.replace("\\", "/")
                                    data['notebook'][0]['file_to_parse'][i] = file_path

                            example = Example(
                                data["notebook"][0]['title'],
                                example_headfix + '/' + dirr,
                                data['notebook'][0]['application domain'].split(" -> "),
                                data['notebook'][0]['description'],
                                data['notebook'][0]['file_to_parse']
                            )

                            # Find the associated app by comparing tree paths
                            associated_app = None
                            for app in self._apps:
                                if example.tree() == app.tree():
                                    associated_app = app
                                    break

                            # Associate the example with the app
                            example.set_app(associated_app)

                            self._examples.append(example)
                    except Exception as e:
                        pass
            break
        
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
        self._examples = []
    
    def name(self):
        return self._name
    
    def path(self):
        return self._path
    
    def tree(self):
        return self._tree
    
    def des(self):
        return self._des
    
    def examples(self):
        return self._examples
    
    def add_example(self, example):
        self._examples.append(example)
    
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
        self._examples = []
        
    
    def name(self):
        return self._name
    
    def path(self):
        return self._path
    
    def tree(self):
        return self._tree
    
    def des(self):
        return self._des
    
    def examples(self):
        return self._examples
    
    def add_example(self, example):
        self._examples.append(example)


class Example:
    def __init__(self, name, path, tree,des,file_to_parse):
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
        self._file_to_parse =file_to_parse
    
    def name(self):
        return self._name
    
    def path(self):
        return self._path
    
    def tree(self):
        return self._tree
    
    def des(self):
        return self._des
    
    def file_to_parse(self):
        return self._file_to_parse     
    
    def has_same_tree_as_app(self, app):
        """
        Check if the example has the same tree path as the given app.

        Parameters
        ----------
        app : App
            The app to compare the tree path with.

        Returns
        -------
        bool
            True if the example has the same tree path as the app, False otherwise.
        """
        return self._tree == app.tree()
    
    def set_app(self, app):
        """
        Set the associated app for the example.

        Parameters
        ----------
        app : App
            The associated app.
        """
        self._app = app
        
    def has_app(self, apps):
        """
        Check if the example has an associated app.

        Parameters
        ----------
        apps : list
            List of App objects

        Returns
        -------
        bool
            True if an associated app is found, False otherwise
        """
        for app in apps:
            if self._tree == app.tree():
                return True
        return False
    
    def associated_app(self, apps):
        """
        Get the associated app of the example.

        Parameters
        ----------
        apps : list
            List of App objects

        Returns
        -------
        App or None
            The associated App object if found, None otherwise
        """
        for app in apps:
            if self._tree == app.tree():
                return app
        return None
    
if __name__ == valid_name:

    p = pysearch(methods_path, applications_path, problems_path)
    p._search()
    
    
    method_nodes = []
    
    for method in p._methods:
        print(method.name())
        print(method.path())
        print(method.tree())
        print(method.des())
        method_nodes.append(method.tree())
        
    
    # Assuming p is an instance of pysearch
    examples = p.examples()
    apps = p.aps()

    for example in examples:
        associated_app = None
        associated_method = None
        
        if example.has_app(apps):
            print("Example:", example.name())
            print("Associated App found.")
            for app in apps:
                if example.tree() == app.tree():
                    associated_app = app
                    associated_app.add_example(example)
                    break
        else:
            print("Example:", example.name())
            print("No associated app found.")

        # Define a regular expression pattern to match the contents of the set_params function
        set_params_pattern = r'set_params\((.*?)\)'

        for file_path in example.file_to_parse():
            if file_path is not None and os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    file_contents = file.read()

                    # Extract the contents of the set_params function using regular expression
                    set_params_match = re.search(set_params_pattern, file_contents)

                    if set_params_match:
                        set_params_contents = set_params_match.group(1)

                        # Extract the value of the 'method' parameter
                        method_match = re.search(r'method=(.*?)(?:,|\))', set_params_contents)

                        if method_match:
                            method_value = method_match.group(1)
                            print(f"Method value in set_params function of file: {file_path} is '{method_value}'")
                            
                            for method in p._methods:
                                if example.tree() == method.tree():
                                    associated_method = method
                                    associated_method.add_example(example)
                                    break
                        else:
                            print(f"No 'method' parameter found in set_params function of file: {file_path}")

                    else:
                        print(f"No match found in file: {file_path}")
            else:
                print(f"File does not exist: {file_path}")