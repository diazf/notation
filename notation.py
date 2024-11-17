#!/opt/homebrew/bin/python3
import argparse
import json
import sys
def parse_json(file_path):
    """
    Recursively parses a JSON file, handling nested inclusions.

    Args:
        file_path: Path to the JSON file.

    Returns:
        A list of notations.
    """

    with open(file_path, 'r') as f:
        data = json.load(f)
    
    includes=[]
    for include in data.get('includes', []):
        _notations,_caption,_includes = parse_json(include)
        includes.append(_notations)
        for _include in _includes:
            includes.append(_include)

    return data.get('notation', []), data.get('caption', None), includes

def print_table(notations,caption,includes):
    included_notation={}
    for include in includes:
        for notation in include:
            if len(notation) > 0:
                included_notation[notation["name"]] = notation
    print("\\begin{table}")
    if caption is not None:
        print("\\caption{%s}"%caption)
    print("\\begin{tabular}{ll}")
    lastempty=True
    for notation in notations:
        notation_ = notation
        name = notation_["name"] if "name" in notation_ else None
        if (name is not None) and (name in included_notation):
            if "definition" in notation_:
                print(f"ERROR: symbol {name} redefined")
                sys.exit()
            for k in ["tabname", "description"]:
                if k not in notation_ and k in included_notation[name]:
                    notation_[k] = included_notation[name][k] 
            notation_["describe"] = True
        if len(notation_) == 0:
            if lastempty is False:
                print("\\\\")
            lastempty = True
        elif ("describe" not in notation_) or (notation_["describe"]):
            name = notation_["tabname"] if "tabname" in notation_ else f"\\{name}"
            print("$%s$\t&\t%s\t\\\\"%(name,notation_["description"]))
            lastempty = False
    print("\\end{tabular}")
    print("\\end{table}")

def print_macros_(notations):
    for notation in notations:
        if "definition" not in notation:
            continue
        if len(notation) > 0 and ("define" not in notation or notation["define"] is True):
            if "operator" in notation and notation["operator"] is True:
                print("\\DeclareMathOperator{\\%s}{%s}"%(notation["name"],notation["definition"]))
            elif "operator*" in notation and notation["operator*"] is True:
                print("\\DeclareMathOperator*{\\%s}{%s}"%(notation["name"],notation["definition"]))
            else:
                print("\\newcommand{\\%s}[%d]{%s}"%(notation["name"],notation["args"] if "args" in notation else 0,notation["definition"]))

def print_macros(notations,includes):
    for include in includes:
        print_macros_(include)
    print_macros_(notations)

def main():
    parser = argparse.ArgumentParser(description='create notation.')
    parser.add_argument('-I', dest='input', help='json file')
    parser.add_argument('-t', dest='table', action='store_true')  

    args = parser.parse_args()
    notations,caption,includes = parse_json(args.input)

    if args.table:
        print_table(notations,caption,includes)
    else:
        print_macros(notations,includes)


if __name__ == '__main__':
    main()