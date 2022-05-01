import tensorflow as tensorflow
from tensorflow import keras
import numpy as np
import os
import matplotlib as mpl 
import matplotlib.pyplot as plt
import pickle
from PIL import Image
import requests

model = None

### Implement train logic with modifiable parameter list
def train_model(_input, params):
    global model
    input = np.array(_input)
    ### preprocess
    X_train_full=input[:,0:-1]
    y_train_full=input[:,-1]
    X_train_full=X_train_full.reshape(60000,28,28)
    X_train, X_valid = X_train_full[:-5000], X_train_full[-5000:]
    y_train, y_valid = y_train_full[:-5000], y_train_full[-5000:]
    # data normalization
    X_mean = X_train.mean(axis=0, keepdims=True)
    X_std = X_train.std(axis=0, keepdims=True) + 1e-7
    X_train = (X_train - X_mean) / X_std
    X_valid=(X_valid - X_mean) / X_std
    X_train = X_train[..., np.newaxis]
    X_valid = X_valid[..., np.newaxis]

    model = keras.models.Sequential([
        keras.layers.Conv2D(64, 7, activation="relu", padding=params[2], input_shape=params[10]),
        keras.layers.MaxPooling2D(params[7]),
        keras.layers.Conv2D(128, 3, activation="relu", padding=params[3]),
        keras.layers.Conv2D(128, 3, activation="relu", padding=params[4]),
        keras.layers.MaxPooling2D(params[8]),
        keras.layers.Conv2D(256, 3, activation="relu", padding=params[5]),
        keras.layers.Conv2D(256, 3, activation="relu", padding=params[6]),
        keras.layers.MaxPooling2D(params[9]),
        keras.layers.Flatten(),
        keras.layers.Dense(128, activation="relu"),
        keras.layers.Dropout(params[0]),
        keras.layers.Dense(64, activation="relu"),
        keras.layers.Dropout(params[1]),
        keras.layers.Dense(10, activation="softmax"),
    ])

    ### train 
    model.compile(loss="sparse_categorical_crossentropy", optimizer="nadam", metrics=["accuracy"])
    histroy = model.fit(X_train, y_train, epochs=1, validation_data=(X_valid, y_valid))

    

### Implement test logic with trained model
def test_model(input):
    global model
    y_pred=model.predict(input)
    pred_index=y_pred.argmax()
    
    class_val={0 : 'T-shirt/top'
    ,1 : 'Trouser'
    ,2 : 'Pullover'
    ,3 : 'Dress'
    ,4 : 'Coat'
    ,5 : 'Sandal'
    ,6 : 'Shirt'
    ,7 : 'Sneaker'
    ,8 : 'Bag'
    ,9 : 'Ankel boot'}

    return class_val[pred_index]
    ### 

### Implement running logic 
def run_train():
    # input = open("./dataset.pickle") # Here you must use pickle
    with open('./data1.pickle', 'rb') as f:
        full_list = pickle.load(f)
    full_np_array=full_list
    input=full_np_array
    dropout_ratio=[0.5,0.5]
    padding=['same','same','same','same','same']
    pool_size=[2,2,2]
    input_shape = [28,28,1]
    
    params = [ 0.5,0.5, "same","same","same","same","same", 2,2,2, [28,28,1]] # Put default parameters here
    # dropout ratio1, dropout_ratio2 
    # padding1, padding2, padding3, padding4, padding5, 
    # pool_size1, pool_size2, pool_size3

    ### we will intercept here
    INTERCEPT_REGION
    ###
    
    train_model(input, params)

def run_test(img): # img is image location
    im = Image.open(requests.get(img, stream=True).raw)
    a=28
    im=im.resize((a,a))
    pix=np.array(im)
    pix=pix[:,:,0]
    pix = pix.reshape(-1,a,a,1)

    return test_model(pix)

run_train()
run_test('https://i.discogs.com/YCopd9B5j4KEu0_mA-L8GirzXpRoHKAFJjDEkntsRTM/rs:fit/g:sm/q:90/h:600/w:600/czM6Ly9kaXNjb2dz/LWRhdGFiYXNlLWlt/YWdlcy9BLTIyMjYz/MDYtMTU5NzMzMjM5/Mi03MzMwLmpwZWc.jpeg')