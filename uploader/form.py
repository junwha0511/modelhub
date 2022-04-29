### Implement train logic with modifiable parameter (max: p10)
def train_model(input, p1, p2, p3, ...):
    ### preprocess

    model = Sequential([
        '''
        Example:
        keras.layers.Conv2D(256, 3, activation="relu", padding=p3) <- here, user can modify p3
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
    input = open("./dataset.pickle") # Here you must use pickle
    p1 = ...
    p2 = ...
    ...
    
    ### we will intercept here
    train_model(input, p1, p2, p3, ...)

def run_test(img):
    return test_model(img)