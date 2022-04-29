from flask import Flask, jsonify, request
from threading import Thread
import requests as http
import importlib.util


app = Flask(__name__)

tid = 0
img_queues = {}
end_queues = {}
out_queues = {}

def model_thread(_tid, params):
   
    global img_queues, end_queues, out_queues
    img_queues[_tid] = []
    out_queues[_tid] = []
    end_queues[_tid] = []

    ### Injection: TODO: implement!!
    with open("user_code{}.py".format(_tid), "r") as f:
        code = f.read()
    injection_code = ""
    for i in range(len(params)):
        injection_code += "    params[{}] = {}\n".format(i, params[i])
    code = code.replace("    INTERCEPT_REGION", injection_code) 
    with open("user_code{}.py".format(_tid), "w") as f:
        f.write(code)
    user_code = importlib.import_module("user_code{}".format(_tid))
    ### Run
    # exec("import user_code{} as user_code".format(_tid))
    user_code.run_train()
    end_queues[_tid].append(True)

    print("[DAEMON] waiting image")
    while len(img_queues[_tid]) == 0:
        pass
    img = img_queues[_tid].pop()
    print("[DAEMON] received img")
    ### Write
    output = user_code.run_test(img)
    out_queues[_tid].append(output)
    print("[DAEMON] queues released")
    ### Release
    del img_queues[_tid]
    del end_queues[_tid]


'''
{
    code: link
    dataset: link
    params: [{"value":xxx, "type":xxx}, {"value":xxx, "type":xxx}, {"value":xxx, "type":xxx}, ...]
}
'''
@app.route('/train', methods=["POST"])
def train():
    global tid, end_queues, out_queues
    # return jsonify({"res": 0})

    # try:
    ### save code & data -> inject -> import code -> train -> create thread -> return tid 
    tid += 1
    _tid = tid
    
    json_data = request.get_json()

    params_info = json_data["params"]
    params = []
    for i in range(len(params_info)):
        type_info = params_info[i]["type"]
        value = params_info[i]["value"]
        if type_info == "string":
            params.append(str(value))
        elif type_info == "int":
            params.append(int(value))
        elif type_info == "float":
            params.append(float(value))
        elif type_info.find("tuple-") != -1:
            params.append(list(map(int, value.strip("(").strip(")").split(","))))
        elif type_info.find("bool"):
            if value == "True" or value == "true":
                params.append(True)
            elif value == "False" or value == "false":
                params.append(False)
        else:
            return jsonify({"response": "400 BAD PARAM TYPE INFO"}), 400
        
    print(params)
    code = http.get(json_data['code'], allow_redirects=True).content
    dataset = http.get(json_data['dataset'], allow_redirects=True).content
    thread = Thread(target=model_thread, args=(_tid, params))
    with open("./user_code{}.py".format(_tid), "wb") as f:
        f.write(code)
    with open("./dataset{}.pickle".format(_tid), "wb") as f:
        f.write(dataset)
    thread.daemon = True
    thread.start()
    print("[TRAIN] Thread created")
    while not (_tid in end_queues):
        pass
    print("[TRAIN] end_queue created")
    while len(end_queues[_tid]) == 0:
        pass
    print("[TRAIN] train complete")
    if end_queues[_tid].pop():
        return jsonify({"model_id": _tid})
    #     return jsonify({"model_id": -1})
    # except:
    #     return jsonify({"model_id": -1})

'''
{
    model_id: int
    img: url
}
'''
@app.route('/test', methods=["POST"])
def test():
    global tid, img_queues
    # return jsonify({"res": 0})
    # try:
    json_data = request.get_json()
    _tid = json_data['model_id']
    img_url = json_data['img']
    img = http.get(img_url, allow_redirects=True)
    img_queues[_tid].append(img)
    while len(out_queues[_tid]) == 0:
        pass
    result = out_queues[_tid].pop()
    del out_queues[_tid]
    return jsonify({"output": result})
    # except:
    #     return jsonify({"output": -1})

# @app.route("/testserver", methods=["GET"])
# def testserver():
#     return jsonify({"res": 0})
    
if __name__ == "__main__":
    app.run(port=9080, debug=True)