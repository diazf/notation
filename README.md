# notation.py

for latex authors interested in maintaining notation in a json file that can be used to generate definitions files and notation tables.

## structure of a notations json

a json dictionary consisting of a single entry `notation` that is a list of notation definitions.  a notation definition consists of the following mandatory fields,
   * `name`: the notation name; should be unique to the project
   * `definition`: escaped latex defining the symbol (what would go in the definition section of newcommand).
   * `description`: escaped latex describing the symbol; this will be printed in the table

and the following optional fields,
   * `tabname`: symbol name to be printed in the table (default: name)
   * `describe`: boolean indicating if the symbol should be included in the notation table (default: true)
   * `define`: boolean indicating if the symbol should be defined as a new command (default: true)
   * `args`: number of arguments that the command will have (default: 0)

the top level dictionary can include an optional `caption` field to contain the notation table caption.

## usage

to generate notation definitions,
```
./notation.py -I example.json
```
to generate a notation table,
```
./notation.py -I example.json -t 
```