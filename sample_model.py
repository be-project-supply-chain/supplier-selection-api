import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import statsmodels.api as sm
import pickle

def create_model():
    data = pd.read_csv("F:/palak study material/sem 6/pracs/ML/airfoil-noise-data.csv")

    x = data.drop(['SoundPressure'], axis=1)
    y = data['SoundPressure']

    
    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.2, random_state = 0)

    lm = LinearRegression()
    model = lm.fit(x_train, y_train)

    filename = 'sample_model.sav'
    
    pickle.dump(model , open(filename, 'wb'))





def load_model():
    data = pd.read_csv("F:/palak study material/sem 6/pracs/ML/airfoil-noise-data.csv")

    x = data.drop(['SoundPressure'], axis=1)
    y = data['SoundPressure']

    
    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.2, random_state = 0)

    filename = 'sample_model.sav'

    loaded_model=pickle.load(open(filename, 'rb'))
    predictions = loaded_model.predict(x_test)

    print(predictions)

    from sklearn.metrics import r2_score
    return (r2_score(y_test, predictions))
    
if __name__ == '__main__':
    filename = 'sample-model.sav'
    create_model();
    # print('model created successfully');
    # score=load_model()
    # print(score)

