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
            


    
if __name__ == "__main__": 
    methods_path = "cofi/src/cofi/tools"
    applications_path = "espresso/contrib"
    problems_path = "cofi-examples/examples"
    ignore_list = ['__init__.py', '_base_inference_tool.py']

    p = pysearch(methods_path, applications_path, problems_path)
    p._search()