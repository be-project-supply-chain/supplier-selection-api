import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pyltr
from sklearn.model_selection import train_test_split
import keras
from keras.models import Sequential
from keras.layers import Dense
import pickle


def create_model():
    dataset = pd.read_csv('sample-data.csv')

    # X = dataset.iloc[:,dataset.columns!='overall_ratings' && dataset.columns!='company_name'].values
    y = dataset.iloc[ : , 14 ].values
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

    model = Sequential()

    model.add(Dense(output_dim = 14, init = 'uniform', activation = 'relu', input_dim = 14))
    model.add(Dense(output_dim = 14, init = 'uniform', activation = 'relu'))
    model.add(Dense(output_dim = 14, init = 'uniform', activation = 'relu'))
    model.add(Dense(output_dim = 1, init = 'uniform', activation = 'relu'))
    
    model.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics = ['accuracy'])

    model.fit(X_train, y_train, batch_size = 50, nb_epoch = 200)

    filename='neural_model.sav'

    pickle.dump(model , open(filename, 'wb'))

def use_model():
    filename='neural_model.sav'
    loaded_model=pickle.load(open(filename, 'rb'))

    dataset = pd.read_csv('real_data.csv')
    # print(dataset.head())

    X = dataset.iloc[:,dataset.columns!='company_name'].values
    # print(X.head())
    # y = dataset.iloc[ : , 14 ].values
    y_pred = loaded_model.predict(X[0:1])
    print(y_pred[0])

def call_from_api(loc1, truck1 , hand1 ):
    dataset = pd.read_csv('real_data.csv')
    loc=[loc1]
    hand=[hand1]
    truck=[truck1]
    # print(dataset)
    output=dataset[dataset.location.isin(loc) & dataset.hand_delivered.isin(hand) & dataset.truck_delivered.isin(truck)]
    # print(output)
    o1=output.sort_values(by=["overall_ratings"] , ascending=[False]  )
    # print(o1)
    return o1





    
if __name__ == '__main__':
    # create_model();
    # use_model()
    call_from_api(2 , 1 , 0)
