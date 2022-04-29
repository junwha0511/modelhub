import pickle

### Implement train logic with modifiable parameter list
def train_model(input, params):
    ### preprocess
    with open("./log", "w") as f:
        f.write(str(input))
        f.write("\n")
        f.write("Ha...")
        f.write("\n")
        f.write(str(params))
    
    ### train 
    

### Implement test logic with trained model
def test_model(input):
    ### 
    pass 

### Implement running logic 
def run_train():
    f = open("./dataset.pickle", "rb") # Here you must use pickle
    input = pickle.load(f)
    f.close()
    params = [1, 3, 2] # Put default parameters here
    
    ### we will intercept here, don't remove this region!
    INTERCEPT_REGION
    ###
    train_model(input, params)

def run_test(img):
    return test_model(img)