import pickle

### Implement train logic with modifiable parameter list
def train_model(input, params):
    ### preprocess

    model = Sequential([
        '''
        Example:
        keras.layers.Conv2D(256, 3, activation="relu", padding=params[3]) <- here, user can modify params[3]
        '''
        ### Implement model here
    ])

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

    params = [ ... ] # Put default parameters here
    
    ### we will intercept here, don't remove this region!
    INTERCEPT_REGION
    ###
    train_model(input, params)

def run_test(img):
    return test_model(img)