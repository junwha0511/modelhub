from flask import Flask, jsonify, request, _app_ctx_stack
from threading import Thread
import requests as http
import importlib.util
import sqlite3
import boto3
from dotenv import load_dotenv
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
load_dotenv(verbose=True)

ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
SESSION_TOKEN = os.getenv('SESSION_TOKEN')

s3 = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    # aws_session_token=SESSION_TOKEN
)

BUCKET_NAME = "hexas3bucket"
DATABASE = './db.sqlite3'

layer_parsed_info1 = [{'name': 'Conv2D', 'modifiable_params_info': [{'name': 'padding', 'type': 'string', 'index': 3}, {'name': 'input_shape', 'type': 'tuple-n', 'index': 4}], 'params': [{'name': 'filters', 'value': '64'}, {'name': 'kernel_size', 'value': ' 7'}, {'name': 'activation', 'value': '"relu"'}, {'name': 'padding', 'value': 'same'}, {'name': 'input_shape', 'value': [28, 28, 1]}]}, {'name': 'MaxPooling2D', 'modifiable_params_info': [{'name': 'pool_size', 'type': 'int', 'index': 0}], 'params': [{'name': 'pool_size', 'value': 2}]}, {'name': 'Conv2D', 'modifiable_params_info': [{'name': 'padding', 'type': 'string', 'index': 3}], 'params': [{'name': 'filters', 'value': '128'}, {'name': 'kernel_size', 'value': ' 3'}, {'name': 'activation', 'value': '"relu"'}, {'name': 'padding', 'value': 'same'}]}, {'name': 'Conv2D', 'modifiable_params_info': [{'name': 'padding', 'type': 'string', 'index': 3}], 'params': [{'name': 'filters', 'value': '128'}, {'name': 'kernel_size', 'value': ' 3'}, {'name': 'activation', 'value': '"relu"'}, {'name': 'padding', 'value': 'same'}]}, {'name': 'MaxPooling2D', 'modifiable_params_info': [{'name': 'pool_size', 'type': 'int', 'index': 0}], 'params': [{'name': 'pool_size', 'value': 2}]}, {'name': 'Conv2D', 'modifiable_params_info': [{'name': 'padding', 'type': 'string', 'index': 3}], 'params': [{'name': 'filters', 'value': '256'}, {'name': 'kernel_size', 'value': ' 3'}, {'name': 'activation', 'value': '"relu"'}, {'name': 'padding', 'value': 'same'}]}, {'name': 'Conv2D', 'modifiable_params_info': [{'name': 'padding', 'type': 'string', 'index': 3}], 'params': [{'name': 'filters', 'value': '256'}, {'name': 'kernel_size', 'value': ' 3'}, {'name': 'activation', 'value': '"relu"'}, {'name': 'padding', 'value': 'same'}]}, {'name': 'MaxPooling2D', 'modifiable_params_info': [{'name': 'pool_size', 'type': 'int', 'index': 0}], 'params': [{'name': 'pool_size', 'value': 2}]}, {'name': 'Flatten', 'modifiable_params_info': [], 'params': []}, {'name': 'Dense', 'modifiable_params_info': [], 'params': [{'name': 'units', 'value': '128'}, {'name': 'activation', 'value': '"relu"'}]}, {'name': 'Dropout', 'modifiable_params_info': [{'name': 'rate', 'type': 'float', 'index': 0}], 'params': [{'name': 'rate', 'value': 0.5}]}, {'name': 'Dense', 'modifiable_params_info': [], 'params': [{'name': 'units', 'value': '64'}, {'name': 'activation', 'value': '"relu"'}]}, {'name': 'Dropout', 'modifiable_params_info': [{'name': 'rate', 'type': 'float', 'index': 0}], 'params': [{'name': 'rate', 'value': 0.5}]}, {'name': 'Dense', 'modifiable_params_info': [], 'params': [{'name': 'units', 'value': '10'}, {'name': 'activation', 'value': '"softmax"'}]}]

tid = 1
mid = 3
img_queues = {}
end_queues = {}
out_queues = {}

def get_db():
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(DATABASE)
    return top.sqlite_db

def create_model_table():
    con = get_db()
    cur = con.cursor()
    cur.execute("CREATE TABLE MODEL(id INTEGER, layer_info TEXT, code_dir TEXT, data_name TEXT, data_dir TEXT) ")
    con.commit()
def create_data_table():
    con = get_db()
    cur = con.cursor()
    cur.execute("CREATE TABLE DATA(name TEXT, data_dir TEXT) ")
    con.commit()

def get_model_by_id(mid):
    con = get_db()
    cur = con.cursor()
    cur.execute('SELECT * FROM MODEL WHERE id =?',(mid,))
    return cur.fetchone()

def get_model_by_name(name):
    con = get_db()
    cur = con.cursor()
    cur.execute('SELECT * FROM MODEL WHERE name =?',(name,))
    return cur.fetchone()

def get_all_model():
    con = get_db()
    cur = con.cursor()
    cur.execute('SELECT * FROM MODEL')
    return cur.fetchall()

def get_all_data():
    con = get_db()
    cur = con.cursor()
    cur.execute('SELECT * FROM DATA')
    return cur.fetchall()

def get_data_by_name(name):
    con = get_db()
    cur = con.cursor()
    cur.execute('SELECT * FROM DATA WHERE name =?',(name,))
    return cur.fetchone()

def insert_data(data_name, data_dir):
    con = get_db()
    cur = con.cursor()
    cur.executemany("INSERT INTO DATA(name, data_dir) VALUES (?,?)", (data_name, data_dir))
    con.commit()

def insert_model(mid, layer_info, code_dir, data_name, data_dir):
    con = get_db()

    # upload_file(code_dir, str(mid)+".py")
    # upload_file (data_dir, data_name+".pickle")

    insert_data(data_name, data_dir)
    cur = con.cursor()
    cur.executemany("INSERT INTO MODEL(id, layer_info, code_dir, data_name, data_dir) VALUES (?,?,?,?,?,?)",  (mid, layer_info, code_dir, data_name, data_dir))
    con.commit()
def upload_file(file_dir, file_name):
    s3.upload_file(file_dir, BUCKET_NAME, file_name)
    a = s3.generate_presigned_url('get_object', Params = {'Bucket': BUCKET_NAME, 'Key': file_name}, ExpiresIn = 10000)


@app.teardown_appcontext
def close_connection(exception):
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()

'''
WEB MODEL
'''
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
    with open("temp{}.py".format(_tid), "w") as f:
        f.write(code)
    user_code = importlib.import_module("temp{}".format(_tid))
    ### Run
    # exec("import user_code{} as user_code".format(_tid))
    user_code.run_train()
    end_queues[_tid].append(True)

    print("[DAEMON] waiting image")
    for i in range(10):
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
    # del out_queues[_tid]

'''
{
    data: [{"value":xxx, "type":xxx}, {"value":xxx, "type":xxx}, {"value":xxx, "type":xxx}, ...]
}
'''
@app.route('/train', methods=["POST"])
def train():
    global tid, end_queues, out_queues
    # return jsonify({"res": 0})

    # try:
    ### save code & data -> inject -> import code -> train -> create thread -> return tid 
    # # tid += 1
    _tid = tid
    json_data = request.get_json()
    print(json_data)

    params_info = json_data["data"]
    params = []
    for i in range(len(params_info)):
        type_info = params_info[i]["type"]
        value = params_info[i]["value"]
        if type_info == "string":
            params.append("\""+str(value)+"\"")
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
    # code = http.get(json_data['code'], allow_redirects=True).content
    # dataset = http.get(json_data['dataset'], allow_redirects=True).content
    thread = Thread(target=model_thread, args=(_tid, params))
    # with open("./user_code{}.py".format(_tid), "wb") as f:
    #     f.write(code)
    # with open("./dataset{}.pickle".format(_tid), "wb") as f:
    #     f.write(dataset)
    thread.daemon = True
    thread.start()
    print("[TRAIN] Thread created")
    while not (_tid in end_queues):
        pass
    print("[TRAIN] end_queue created")

    return jsonify({"mid": _tid})
    # while len(end_queues[_tid]) == 0:
    #     pass
    # print("[TRAIN] train complete")
    # if end_queues[_tid].pop():
    #     return jsonify({"mid": _tid})
    # #     return jsonify({"mid": -1})
    # # except:
    # #     return jsonify({"mid": -1})

'''
{
    mid: int
}
'''
@app.route('/status', methods=["GET"])
def get_status():
    
    _mid = int(request.args.get("mid"))

    if len(end_queues[_mid]) == 0:
        return jsonify({"status": "running"})
    return jsonify({"status": "end"})
'''
{
    mid: int
    img: url
}
'''
@app.route('/test', methods=["POST"])
def test():
    global tid, img_queues
    # return jsonify({"res": 0})
    # try:
    json_data = request.get_json()
    _tid = int(json_data['mid'])
    img_queues[_tid].append(json_data['img'])
    while len(out_queues[_tid]) == 0:
        pass
    result = str(out_queues[_tid].pop())
    
    return jsonify({"output": result})
    # except:
    #     return jsonify({"output": -1})

'''
USER CLI
'''
'''
files: {
    code, data
}
'''
@app.route('/upload', methods=["POST"])
def upload():
    # global mid
    # # code = request.files['code'] 
    # # data = request.files['data']  
    # # # layer_info = json_data['layerInfo'] 
    # # # data_name = json_data['data_name'] 

    mid += 1
    _mid = mid

    data_dir = "./"+"data{}".format(_mid)+".pickle"
    code_dir = "./"+"user_code{}".format(_mid)+".py"

    # code.save(data_dir)
    # data.save(code_dir)
    
    return jsonify({"status": "200", "mid": _mid, "code_dir": code_dir, "data_dir": data_dir})
'''
data: {
    mid: mid
    data_name: string,
    layer_info: JSON,
    code_dir: dir
    data_dir: dir 
}

'''
@app.route('/construct', methods=["POST"])
def construct():
    global mid
    json_data = request.get_json()
    # insert_model(json_data["mid"] , json_data["layer_info"], json_data["code_dir"], json_data["data_name"], json_data["data_dir"])
    if json_data["mid"] > mid: # Error prone
        mid = json_data["mid"]
    
    return jsonify({"status": "200", "mid": json_data["mid"]})

# '''
# WEB VIEW
# '''

# @app.route('/models/list', methods=["GET"])
# def get_model_list():
#     models = get_all_model()
#     print(models)
#     return jsonify({"status": "200"})
# '''
# {
#     "name": string
# }
# '''
# @app.route('/models/search', methods=["GET"])
# def search_model():
#     json_data = request.get_json()
#     model = get_model_by_name(json_data["name"])
#     print(model)
#     return jsonify({"status": "200"})

# @app.route('/data/list', methods=["GET"])
# def get_data_list():
#     data = get_all_data()
#     print(data)
#     return jsonify({"status": "200"})
# '''
# {
#     "name": string
# }
# '''
# @app.route('/data/search', methods=["GET"])
# def search_data():
#     json_data = request.get_json()
#     model = get_model_by_name(json_data["name"])
#     print(model)
#     return jsonify({"status": "200"})

# # @app.route("/testserver", methods=["GET"])
# # def testserver():
# #     return jsonify({"res": 0})
    
if __name__ == "__main__":
    app.run(port=9080)