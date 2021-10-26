import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from data import load_data

print('Loading Data...')
df = load_data()

X = df.drop(columns='target')
y = df['target']

clf = RandomForestClassifier(random_state=42)

# Perform short gridsearch for params
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [4, 8, None],
    'min_samples_leaf': [1, 3, 5]
}
print('Performing GridSearch...')
gsCV = GridSearchCV(clf, param_grid, scoring='accuracy')
gsCV.fit(X, y)

print('Fitting model')
# Fit classifier with best params
clf.set_params(**gsCV.best_params_)
clf.fit(X, y)

# Save model as pickle file
with open('model.pickle', 'wb') as f:
    pickle.dump(clf, f, protocol=pickle.HIGHEST_PROTOCOL)




