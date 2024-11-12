#!/opt/homebrew/bin/python3
import argparse
import json

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
    
    return data.get('notation', []), data.get('caption', None)



def main():
    parser = argparse.ArgumentParser(description='create notation.')
    parser.add_argument('-I', dest='input', help='json file')
    parser.add_argument('-t', dest='table', action='store_true')  

    args = parser.parse_args()
    notations,caption = parse_json(args.input)
    
    if args.table:
        print("\\begin{table}")
        if caption is not None:
            print("\\caption{%s}"%caption)
        print("\\begin{tabular}{ll}")
    lastempty=True
    for notation in notations:
        if args.table:
            if len(notation) == 0 and lastempty is False:
                print("\\\\")
                lastempty = True
            elif ("describe" not in notation) or (notation["describe"]):
                name = notation["tabname"] if "tabname" in notation else f"\\{notation["name"]}"
                print("$%s$\t&\t%s\t\\\\"%(name,notation["description"]))
                lastempty = False
        else:
            if len(notation) > 0 and ("define" not in notation or notation["define"] is True):
                if "operator" in notation and notation["operator"] is True:
                    print("\\DeclareMathOperator{\\%s}{%s}"%(notation["name"],notation["definition"]))
                if "stoperator" in notation and notation["stoperator"] is True:
                    print("\\DeclareMathOperator*{\\%s}{%s}"%(notation["name"],notation["definition"]))
                else:
                    print("\\newcommand{\\%s}[%d]{%s}"%(notation["name"],notation["args"] if "args" in notation else 0,notation["definition"]))

    if args.table:
        print("\\end{tabular}")
        print("\\end{table}")

if __name__ == '__main__':
    main()