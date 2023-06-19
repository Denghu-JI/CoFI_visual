from relation_dict import hirc_tree, insert
from pysearch_tool import pysearch

#please specify those folder!
methods_path = "pysearch_tool/cofi/src/cofi/tools"
applications_path = "pysearch_tool/espresso/contrib"
problems_path = "pysearch_tool/cofi-examples/examples"
ignore_list = ['__init__.py', '_base_inference_tool.py']

ignore = ['slug_test', 'pumping_test', 'simple_regression', '']





def main():
    p = pysearch.pysearch(methods_path,applications_path,problems_path)
    p.search(ignore)
    method_tree = hirc_tree('CoFI')
    apps_tree = hirc_tree('37 Earth Sciences')

    for i in p.mds():
        method_tree = insert(method_tree,i)

    for i in p.aps():
        apps_tree = insert(apps_tree,i)

    cmd = " "
    current_node = apps_tree
    last_node = []

    while cmd != 'exit':
        cmd = input('Whats next?: ')
        if cmd == 'children?':
            if len(current_node.children()) == 0:
                print("you have reached a terminal")
            for i in current_node.children():
                print(i.me())
        elif cmd[:2] == 'go':
            flag = False
            for i in current_node.children():
                if i.me() == cmd [3:]:
                    last_node.append(current_node)
                    current_node = i
                    print("now you are on " + i.me() + ", its children are: ", end = '')
                    for j in i.children():
                        print(j.me() + " | ", end = '')
                    print(" ")
                    flag = True
            if not flag:
                print("no such child!")
        elif cmd == "reset":
            current_node = apps_tree
        elif cmd == "back":
            if len(last_node) == 0:
                print("cannot go back")
            else:
                current_node = last_node.pop()
        elif cmd == "path":
            print(current_node.path())
        elif cmd == "des":
            print(current_node.description())
        elif cmd == "me":
            print(current_node.me())
        elif cmd == "pt":
            print(current_node.parent())
        else:
            print("not a vaild command")

if __name__ == "__main__": 
    main()
