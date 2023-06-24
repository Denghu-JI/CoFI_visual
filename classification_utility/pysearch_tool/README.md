# pysearch
pysearch is a Python module that allows you to search and extract information from code files in specified directories. It provides functionality to search for inference methods, applications, and example problems, and organize them in a hierarchical tree structure.

Installation
To use pysearch, follow these steps:

Clone the repository or download the source code.
Place the pysearch.py file in your project directory or in a location accessible by your Python scripts.
Usage
Initializing pysearch
To use pysearch, you need to import the module and create an instance of the pysearch class. Here's an example:

'''python
from pysearch import pysearch

# Specify the paths to the method, application, and problem directories
method_path = "path/to/methods"
app_path = "path/to/applications"
prob_path = "path/to/problems"
'''

# Create an instance of the pysearch class
p = pysearch(method_path, app_path, prob_path)


# Create an instance of the pysearch class
p = pysearch(method_path, app_path, prob_path)
Searching for Methods and Applications
You can search for inference methods and applications using the search method. The search method takes an optional ignore parameter, which is a list of files to ignore during the search.

Here's an example of searching for methods and applications:

python
Copy code
# Search for methods and applications
ignore_list = ['__init__.py', '_base_inference_tool.py']  # Files to ignore
p.search(ignore_list)

# Retrieve the found methods and applications
methods = p.mds()  # List of found methods
applications = p.aps()  # List of found applications
Searching for Example Problems
You can search for example problems using the search_examples method. Similar to the search method, the search_examples method also takes an optional ignore parameter to ignore specific files during the search.

Here's an example of searching for example problems:

python
Copy code
# Search for example problems
p.search_examples(ignore_list)

# Retrieve the found example problems
problems = p.problems()  # List of found example problems
Building and Printing the Tree Structure
After searching for methods, applications, and example problems, you can build a hierarchical tree structure using the build_tree_from_lists function. This function takes a list of tree paths and returns the root node of the tree.

Here's an example of building and printing the tree structure:

python
Copy code
# Build the tree structure
tree_lists = []
for method in methods:
    tree_lists.append(method.tree())
root_node = build_tree_from_lists(tree_lists)

# Add example problems to the tree nodes
root_node = add_examples_to_tree(root_node, problems)

# Print the tree structure
print_tree(root_node)
The print_tree function will print the tree structure along with the example problems associated with each node.


