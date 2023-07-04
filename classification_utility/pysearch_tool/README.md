# pysearch
pysearch is a Python module that allows you to search and extract information from code files in specified directories. It provides functionality to search for inference methods, applications, and example problems, and organize them in a hierarchical tree structure.

To run the code and perform a search on code repositories, follow the steps below:

Clone the repository or download the code files to your local machine. Link: https://github.com/Denghu-JI/CoFI_visual.git

Navigate to "CoFI_visual\classification_utility\pysearch_tool"

1. Install the required dependencies:

2. Ensure that you have Python installed on your system (Python 3.7 or above is recommended).
The code uses standard Python libraries, so no additional external dependencies need to be installed.

3. Set up the directory structure:

Create the following directories to organize your code repositories:

methods: This directory will contain the files with inference methods.
applications: This directory will contain the files with applications.
problems: This directory will contain the example problem files.
Place your code files in the respective directories based on their type:

Inference methods: Place the files with inference methods in the methods directory.
Applications: Place the files with applications in the applications directory.
Example problems: Place the example problem files in the problems directory.
Update the file paths in the code:

Open the config.py file and update the following variables with the correct paths:
methods_path: The path to the methods directory.
applications_path: The path to the applications directory.
problems_path: The path to the problems directory.
ignore_list: (Optional) If there are any files that you want to exclude from the example search, add their names to this list.

Define the legal node names for each level in legal_node_names.txt

4. Run the code:

Open a terminal or command prompt.
Navigate to the directory where the code files are located.
Execute the following command to run the code: python pysearcj.py.

5. View the results:

After executing the code, it will perform the search and organize the code repositories.
The example tree paths will be printed, showing the hierarchy of examples within the tree structure.
The entire tree structure will be printed, displaying the methods, applications, and example problems in a hierarchical format.

6. Customize and extend the code (optional):

You can modify the code to suit your specific requirements.
For example, you can add additional functionality to parse different types of code files or enhance the search algorithm.


