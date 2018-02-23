import pandas as pd
from dateutil import parser, rrule
import numpy as np
import getDegrees_Y 
import numpy as np
from keras.models import Sequential 
from keras.layers import Dense


def train(temperatures,planet_data,start_date,end_date,x_index,y_index,fs,regressor,bs,eph):

    dates_string = getDegrees_Y.getDateString(start_date,end_date)
    ret = getDegrees_Y.getDegrees_Y(dates_string,temperatures,planet_data,y_index)
    print("Training data :", len(ret["X"]),len(ret["Y"]))

    X_d = ret["X"][:,x_index]

    ##Feature Scaling
    from sklearn.preprocessing import StandardScaler

    ## Scaling for output is not necessary
    if fs:
       sc_X = StandardScaler()
       X_tr = sc_X.fit_transform(X_d)
       y_tr = ret["Y"][:,-1].reshape(-1,1)
    else:
        X_tr = X_d
        y_tr = ret["Y"][:,-1].reshape(-1,1)
        sc_X = None
        sc_Y = None
    
    regressor.fit(X_tr,y_tr,batch_size=bs,epochs=eph)
    
    return {"reg":regressor,"X_tr":sc_X}

def train_test(indep_var_idx,dep_var_idx,feature_scaling,tr_start,tr_end,test_start,test_end,regressor,batch_size,epochs):

   temperatures = pd.read_csv("Chennai_temperature_data.csv")
   planet_data = pd.read_csv("Chennai_PP_data.csv")
    
   ##Training
   reg = train(temperatures,planet_data,tr_start,tr_end,indep_var_idx,dep_var_idx,feature_scaling,regressor,batch_size,epochs)

   ##Testing
   dates_string = getDegrees_Y.getDateString(test_start,test_end)
   ret1 = getDegrees_Y.getDegrees_Y(dates_string,temperatures,planet_data,dep_var_idx)
   print("Test data ", len(ret1["X"]),len(ret1["Y"]))

   X_td = ret1["X"][:,indep_var_idx]

   if feature_scaling:
      X_test = reg["X_tr"].transform(X_td)
   else:
      X_test = X_td

   y_pred = reg["reg"].predict(X_test)

   ##Visualize
   #Needed to inline graphs
   import matplotlib.pyplot as plt

   plt.plot(y_pred,label="pred")

   plt.plot(ret1["Y"][:,-1],label="actual")
   plt.legend()
   
   print("MSE : ", regressor.evaluate(X_test,ret1["Y"][:,-1].reshape(-1,1)))
    
   return plt

if __name__ == "__main__":

   indep_var_idx = [3,4,5,9,13]
   dep_var_idx = 6
   feature_scaling = False

   tr_start = "2010-06-01"
   tr_end = "2014-12-1"

   test_start = "2015-01-01"
   test_end = "2017-12-1"


   regressor = Sequential()
   ## 2 hidden layers with 5 nodes each
   regressor.add(Dense(units=5,kernel_initializer='uniform',activation='relu',input_shape=(len(indep_var_idx),)))
   regressor.add(Dense(units=5,kernel_initializer='uniform',activation='relu'))
   regressor.add(Dense(units=5,kernel_initializer='uniform',activation='relu'))

   ## Output layer 
   regressor.add(Dense(units=1,kernel_initializer='uniform',activation=None))

   print(regressor.summary())

   regressor.compile(optimizer='adam',loss='mean_squared_error')

   plt = train_test(indep_var_idx,dep_var_idx,feature_scaling,tr_start,tr_end,test_start,test_end,regressor,10,50)
   plt.show()
