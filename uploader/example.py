from doctest import DocTestFinder
from email.headerregistry import AddressHeader
from re import S
from signal import SIG_DFL
from this import d
from tkinter.dnd import dnd_start
from attr import asdict


asdfsafsdf
dfsdfs
asdictf
SIG_DFLsdf

json = [{}, {}, {}]

### Implement train logic with modifiable parameter
def train_model(input, param):
    ### preprocess

     model = keras.models.Sequential([
        keras.layers.Conv2D(64, 7, activation="relu", padding="same", input_shape=param[3]),
        keras.layers.MaxPooling2D(2),
        keras.layers.Conv2D(param[0], 3, activation="relu", padding="same"),
        keras.layers.Conv2D(128, 3, activation="relu", padding="same"),
        keras.layers.MaxPooling2D(2),
        keras.layers.Conv2D(256, 3, activation="relu", padding=param[2]),
        keras.layers.Conv2D(256, 3, activation="relu", padding="same"),
        keras.layers.MaxPooling2D(2),
        keras.layers.Flatten(),
        keras.layers.Dense(param[1], activation="relu"),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(64, activation="relu"),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(10, activation="softmax")
    ])

    ### train 
    

### Implement test logic with trained model
def test_model(input):
    ### 
    pass 

### Implement running logic 
def run_train():
    input = open("./dataset.pickle") # Here you must use pickle
    params = [1, 3, 2, 4]
    ### we will intercept here
    train_model(input, params)

def run_test(img):
    return test_model(img)
Sequential()

def run_model(input, p1, p2, p3, p4):
   

    ---
    // optimizer, compile  (shape, asdfdf), run  
input = (./pickle)
p1 = 3
p2 = 4
p3 = 5
p4 = 6
### INJECTED
input = (./pickle) ### from server
p1 = 6
p2 = 5
p3 = 4
p4 = 3
###
run_model(input, p1, p2, p3, p4)
AddressHeaderfs

DocTestFinderas
dnd_start

