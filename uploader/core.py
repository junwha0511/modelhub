from numpy import angle
import layer_info as info
import json
from lib2to3.pgen2.token import STAR
import click
import requests

CODE_DIR = "./example.py"
START_STR = "Sequential(["

layers = []
param_names = [] # Parameter names in top function
param_values = {}
datas = {
}
files = {
 
}

# url = "http://localhost:9080"


# headers = {'content-type':'multipart/form-data'}
# response = requests.post(url,data=datas, headers=headers )
# filepath  = ''
# datasetpath = ''

@click.command()
@click.argument('fpath', type=click.Path(exists=True))
@click.argument('dpath', type=click.Path(exists=True))
@click.argument('dname')
@click.argument('mid')
def main(fpath, dpath, dname, mid):
    CODE_DIR= fpath

    f = open(CODE_DIR, "r")
    code = f.read()
    f.close()
    
    # Find first start point
    layer_start_idx = code.find(START_STR) 
    if layer_start_idx == -1:
        exit()
    layer_start_idx += len(START_STR)  
    # Find # of parameter 
    param_symbol = "params = ["
    start = code.find(param_symbol)+len(param_symbol)
    end = start+code[start:].find("# Put default parameters here")
    n_params = 11 #len(code[start:end].split(","))
    for i in range(0, n_params):
        param_names.append("params[{}]".format(i))

    ### Param Parsing ###
    # for name in param_names:
    #     pos = code.find(name+" = ") + len(name+" = ")
        
    param_values_value = [ 0.5,0.5, "same","same","same","same","same", 2,2,2, [28,28,1]]

    
    for i in range((n_params)):
        param_values[param_names[i]] = param_values_value[i]

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
                if layer_params[i].strip(" ") == param_name:
                    
                    positional_params_types[i]
                    layer_params_info.append({
                        "name": positional_params_names[i],
                        "type": positional_params_types[i],
                        "index": param_names.index(param_name),
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
                    # print(param_names.index(param_name))
                    parsed_params[-1]["value"] = param_values[param_name]
                    layer_params_info.append({
                        "name": keyword,
                        "type": keyword_params_map[keyword],
                        "index": param_names.index(param_name),
                    })

        layer_parsed_info.append({
            "name": layer_name,
            "modifiable_params_info": layer_params_info,
            "params": parsed_params,
        })
    layer_parsed_info = (layer_parsed_info)
   
    # m = MultipartEncoder(
    # fields={'field0': 'value', 'field1': 'value',
    #         'code': (CODE_DIR.split("/")[-1], open(CODE_DIR,'rb'), 'text/plain'),
    #         'data': (dname, open(dpath, 'rb'), 'text/plain'),
    # })
    
    # response = requests.post(url+"/upload", data=m,
    #               headers={'content-type': m.content_type})

    # json_data = response.json()
    for layer in layer_parsed_info:
        print(layer)
    # print(layer_parsed_info)
    # datas['layer_info'] = layer_parsed_info
    # datas['data_name'] = dname
    # datas["code_dir"] = CODE_DIR
    # datas["data_dir"] = dpath
    # datas["mid"] = mid
    
    # response = requests.post(url+"/construct", data=datas)

    # print(response.content)

if __name__ == '__main__':
    main()

