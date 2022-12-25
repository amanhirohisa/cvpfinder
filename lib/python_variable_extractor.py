import ast
import sys
import glob
import os
from pathlib import Path

#
# Visitor for processing variable-related AST nodes
#
class VarNodeVisitor(ast.NodeVisitor):
    def __init__(self, node):
        self.root = node
        self.name_node_list = []
        self.arg_node_list = []
        self.global_node_list = []
        self.listcomp_node_list = []
        self.setcomp_node_list = []
        self.dictcomp_node_list = []
        self.generator_node_list = []
        self.attribute_node_list = []

    def visit_ClassDef(self, node):
        if node == self.root:
            return self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node):
        if node == self.root:
            return self.generic_visit(node)
        return node

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.name_node_list.append(node)
        return node

    def visit_arg(self, node):
        self.arg_node_list.append(node)
        return node

    def visit_Global(self, node):
        self.global_node_list.append(node)
        return node

    def visit_Attribute(self, node):
        if node == self.root:
            return self.generic_visit(node)
        if isinstance(node.ctx, ast.Store):
            self.attribute_node_list.append(node)
        return node

#
# extract the arguments (formal parameters)
# of the function corresponding to the given AST node (as root)
#
def extract_args(root):
    visitor = VarNodeVisitor(root)
    visitor.visit(root)

    arg_list = []
    for node in visitor.arg_node_list:
        if node.arg != 'self':
            arg_list.append(node.arg)

    return arg_list

#
# extract the attributes (class variables)
# of the class corresponding to the given AST node (as root)
#
def extract_attributes(root):
    visitor = VarNodeVisitor(root)
    visitor.visit(root)

    attribute_list= []
    for node in visitor.attribute_node_list:
        if isinstance(node.value, (ast.Attribute, ast.Call, ast.Subscript)):
            continue
        if (isinstance(node.ctx, ast.Store)) and (node.value.id == "self"):
            if node.attr not in attribute_list:
                attribute_list.append(node.attr)

    return attribute_list

#
# extract the local variables appearinng in
# the function correspong to the given AST node (as root);
#
# If there are variables declared with "global" keyword,
# append them to gloval_var_name_list
def extract_variables(root, global_var_name_list):
    visitor = VarNodeVisitor(root)
    visitor.visit(root)

    global_declared_name_list = []
    for node in visitor.global_node_list:
        global_declared_name_list.extend(node.names)
        for name in node.names:
            if name not in global_var_name_list:
                global_var_name_list.append(name)

    variable_name_list = extract_attributes(root)

    for element in visitor.name_node_list:
        if element.id in global_declared_name_list:
            continue
        if element.id in variable_name_list:
            continue
        if element.id == '_':
            continue
        variable_name_list.append(element.id)

    return variable_name_list

#
# create a dictionary storing all variable information found in
# the artifact corresponding to the give AST node (as root);
#
# gloval_var_name_list: the list to buffer the variables declared with "global" keyword;
# queue: the queue to buffer the unprocessed "ClassDef" or "FunctionDef" nodes;
def create_dict(root, global_var_name_list, queue):
    dictionary = { 'node' : root }

    if isinstance(root, ast.Module):
        dictionary['kind'] = 'Module'
        dictionary['name'] = None
        dictionary['begin'] = None
        dictionary['end'] = None
    elif isinstance(root, ast.ClassDef):
        dictionary['kind'] = 'class'
        dictionary['name'] = root.name
        dictionary['begin'] = root.lineno
        dictionary['end'] = root.end_lineno
    elif isinstance(root, ast.FunctionDef):
        dictionary['kind'] = 'func'
        dictionary['name'] = root.name
        dictionary['begin'] = root.lineno
        dictionary['end'] = root.end_lineno
    else:
        dictionary['kind'] = 'unknown'
        dictionary['name'] = None
        dictionary['begin'] = None
        dictionary['end'] = None

    dictionary['classes'] = []
    dictionary['funcs'] = []

    dictionary['vars'] = extract_variables(root, global_var_name_list)
    dictionary['args'] = extract_args(root)

    flag = False
    for node in root.body:
        if isinstance(node, ast.ClassDef):
            flag = True
            dictionary['classes'].append(node)
        if isinstance(node, ast.FunctionDef):
            flag = True
            dictionary['funcs'].append(node)
    if flag:
        queue.append(dictionary)

    return dictionary


#
# print the variable information by traversing the dictionary;
# file: the parsed python file name
#
def print_dict(dictionary, file):
    begin = dictionary['begin']
    end = dictionary['end']
    if dictionary['kind'] == 'Module':
        kind = 'G'
    elif dictionary['kind'] == 'class':
        kind = 'A'
    else:
        kind = 'L'
    for v in dictionary['vars']:
        print(file, kind, v, 'None', begin, end, sep='\t')
    for cls in dictionary['classes']:
        print_dict(cls, file)
    for func in dictionary['funcs']:
        print_dict(func, file)

#
# move the local variables with the prefix "self." to the corresponding
# class's attribute list
def move_self_vars(dictionary, target_dict):
    if dictionary['kind'] == 'class':
        for cls in dictionary['classes']:
            move_self_vars(cls, dictionary)
        for func in dictionary['funcs']:
            move_self_vars(func, dictionary)
    else:
        for cls in dictionary['classes']:
            move_self_vars(cls, target_dict)
        for func in dictionary['funcs']:
            move_self_vars(func, target_dict)

    if dictionary['kind'] == 'func':
        new_var_list = []
        self_var_list = []
        for var in dictionary['vars']:
            if var.startswith('self.'):
                self_var_list.append(var.replace('self.',''))
            else:
                new_var_list.append(var)
        if len(self_var_list) > 0:
            dictionary['vars'] = new_var_list
            for self_var in self_var_list:
                if self_var not in target_dict['vars']:
                    target_dict['vars'].append(self_var)

#####################################################################
# main

# process the command line argumetns
verbose_mode = False
file_or_dir = None
for i in range(1,len(sys.argv)):
    if sys.argv[i] == '-v':
        verbose_mode = True
        continue
    file_or_dir = sys.argv[i]
    break

if file_or_dir is None:
    print('*** [Error] invalid arguments', file=sys.stderr)
    print('  Specify a python file or a directory containing python files!', file=sys.stderr)
    sys.exit(1)

targets = []
if Path.is_file(Path(file_or_dir)):
    targets.append(file_or_dir)
    print('[target file] ' + file_or_dir, file=sys.stderr)
else:
    targets = [p for p in glob.glob(os.path.join(file_or_dir, '**'), recursive=True) if os.path.isfile(p) and p.endswith('.py')]
    print('[target dir] ' + file_or_dir, file=sys.stderr)
    print('(' + str(len(targets)) + ' python files)', file=sys.stderr)

# print headers
print("path", "kind", "name", "type", "begin", "end", sep='\t')

# process each python file
for file in targets:
    if verbose_mode:
        print('Parsing ...', file, file=sys.stderr)
    try:
        root = ast.parse(open(file, encoding="utf-8").read())
    except Exception as e:
        print('*** Error ***', file, file=sys.stderr)
        print(e, file=sys.stderr)
        continue

    global_var_name_list = []
    queue = []
    dictionary = create_dict(root, global_var_name_list, queue)
    dictionary['begin'] = 1
    dictionary['end'] = len(open(file, encoding="utf-8").read().split('\n'))

    while len(queue) > 0:
        unprocessed = queue.pop(0)
        for i, node in enumerate(unprocessed['classes']):
            unprocessed['classes'][i] = create_dict(node, global_var_name_list, queue)
        for i, node in enumerate(unprocessed['funcs']):
            unprocessed['funcs'][i] = create_dict(node, global_var_name_list, queue)

    global_variable = dictionary['vars']
    for elt in global_var_name_list:
        if not elt in global_variable:
            global_variable.append(elt)

    move_self_vars(dictionary, None)

    print_dict(dictionary, file)
