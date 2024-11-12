# notation.py

for latex authors interested in maintaining notation in a json file that can be used to generate definitions files and notation tables.

## structure of a notations json

a json dictionary consisting of a single entry `notation` that is a list of notation definitions.  a notation definition consists of the mandatory `name` field which declares the notation name; this should be unique to the project.  

if you are defining a new symbol, you must include a `definition` field with the escaped latex defining the symbol (what would go in the definition section of newcommand).  if you are _not_ defining a new symbol (e.g., if you just want to include a classic symbol in the notation table), set `define` to `false`. if your symbol takes arguments, include the count in `args` field, which defaults to 0. if you are defining an operator, then set `operator` to `true` (for `DeclareMathOperator`) or `stoperator` to `true` (for `DeclareMathOperator*`). 

if you want a symbol in the notation table, you must include a `description` field with the escaped latex describing the symbol (this will be printed in the table).  if you do _not_ want the symbol in the notation table (e.g., if it's a support symbol or rarely used), set `describe` to `false`.  if you want the symbol notation in the table to be different from the simple symbol (e.g., if you want to show the function signature), define it using escaped latex in the `tabname` field.  


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