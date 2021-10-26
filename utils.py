import pickle

# Clf mapping dict for predicitons
clf_dict = {
    0: 'Setosa',
    1: 'Versicolor',
    2: 'Virginica'
}

# Load model
def load_model():
    '''
    Loads model
    '''
    with open('model.pickle', 'rb') as f:
        clf = pickle.load(f)
    
    return clf