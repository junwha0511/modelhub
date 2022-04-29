from numpy import angle
import layer_info as info
import json

CODE_DIR = "./example.py"
START_STR = "Sequential(["

layers = []
param_names = ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10"] # Parameter names in top function
param_values = {}

### Code Parsing ###
f = open(CODE_DIR, "r")
code = f.read()
f.close()

# Find first start point
layer_start_idx = code.find(START_STR) 
if layer_start_idx == -1:
    exit()
layer_start_idx += len(START_STR)

angle_bracket_cnt = 0
square_bracket_cnt = 1
i = layer_start_idx
start_idx = layer_start_idx
scanning = True
while True:
    if scanning == True:
        if code[i] == " " or code[i] == "\n" or code[i] == ",":
            pass
        else:
            start_idx = i
            scanning = False
    if code[i] == "(":
        angle_bracket_cnt += 1
    elif code[i] == ")":
        angle_bracket_cnt -= 1
        if angle_bracket_cnt == 0:
            layers.append(code[start_idx:i+1])      
            scanning = True      
    elif code[i] == "[":
        square_bracket_cnt += 1
    elif code[i] == "]":
        square_bracket_cnt -= 1
        if square_bracket_cnt == 0:
            break
    i += 1
    
### Param Parsing ###
for name in param_names:
    pos = code.find(name+" = ") + len(name+" = ")
    param_values[name] = code[pos:].split("\n")[0]


### Layer Parsing ###
layer_parsed_info = []
for layer in layers:
    parsed_params = []
    splitted_layer = layer.split("(")
    layer_name = splitted_layer[0]
    layer_params = "".join(splitted_layer[1:])
    layer_name = layer_name.split(".")[-1]
    layer_params = layer_params.strip("(").strip(")").split(",")
    
    layer_params_info = []

    # try:
    layer_info = info.positional_params_INFO[layer_name]
    n_positional = layer_info["n_positional"]
    positional_params_names = layer_info["positional_params_names"]
    positional_params_types = layer_info["positional_params_types"]
    keyword_params_map = layer_info["keyword_params_map"]

    # Parse Positional Parameters
    for i in range(n_positional):
        parsed_params.append({"name": positional_params_names[i], "value": layer_params[i]})
        for param_name in param_names:
            if layer_params[i] == param_name:
                positional_params_types[i]
                layer_params_info.append({
                    "name": positional_params_names[i],
                    "type": positional_params_types[i],
                    "index": i,
                })
                parsed_params[-1]["value"] = param_values[param_name]
                break
    # Parse Keyword Parameters
    for i in range(n_positional, len(layer_params)):
        if layer_params[i].strip(" ") == "":
            continue
        (keyword, value) = layer_params[i].split("=")
        keyword = keyword.strip(" ")
        value = value.strip(" ")
        parsed_params.append({"name": keyword, "value": value})
        for param_name in param_names:
            
            if value == param_name:
                parsed_params[-1]["value"] = param_values[param_name]
                layer_params_info.append({
                    "name": keyword,
                    "type": keyword_params_map[keyword],
                    "index": i,
                })

    layer_parsed_info.append({
        "name": layer_name,
        "modifiable_params_info": layer_params_info,
        "params": parsed_params,
    })

layer_parsed_info = json.dumps(layer_parsed_info)
print(layer_parsed_info)