import pandas as pd
from dateutil import parser, rrule
import numpy as np
import getDegrees_Y 
import numpy as np


def train(temperatures,planet_data,start_date,end_date,x_index,y_index,fs):

    dates_string = getDegrees_Y.getDateString(start_date,end_date)
    ret = getDegrees_Y.getDegrees_Y(dates_string,temperatures,planet_data,y_index)
    print("Training data :", len(ret["X"]),len(ret["Y"]))

    #Keep mars,mercury,moon,sun,venus
    X_d = ret["X"][:,x_index]

    ##Feature Scaling
    from sklearn.preprocessing import StandardScaler

    if fs:
       sc_X = StandardScaler()
       X_tr = sc_X.fit_transform(X_d)
       sc_Y = StandardScaler()
       y_tr = sc_Y.fit_transform(ret["Y"][:,-1].reshape(-1,1))
    else:
        X_tr = X_d
        y_tr = ret["Y"][:,-1].reshape(-1,1)
        sc_X = None
        sc_Y = None
    
    #train
    from sklearn.linear_model import LinearRegression
    regressor = LinearRegression()
    regressor.fit(X_tr,y_tr)
    
    #Print coeff
    print("alpha = ", regressor.intercept_)
    print(pd.DataFrame(np.column_stack((np.array(regressor.coef_)[0],np.array(ret["X_keys"][x_index])))))
    
    return {"reg":regressor,"X_tr":sc_X,"y_tr":sc_Y}

def train_test(indep_var_idx,dep_var_idx,feature_scaling,tr_start,tr_end,test_start,test_end):

   temperatures = pd.read_csv("Chennai_temperature_data.csv")
   planet_data = pd.read_csv("Chennai_PP_data.csv")
    
   ##Training
   reg = train(temperatures,planet_data,tr_start,tr_end,indep_var_idx,dep_var_idx,feature_scaling)

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
   import matplotlib.pyplot as plt

   if feature_scaling:
      plt.plot(reg["y_tr"].inverse_transform(y_pred),label="pred")
   else:
      plt.plot(y_pred,label="pred")

   plt.plot(ret1["Y"][:,-1],label="actual")
   plt.legend()
   
   return plt

if __name__ == "__main__":

   indep_var_idx = [3,4,5,9,13]
   dep_var_idx = 6
   feature_scaling = False

   tr_start = "2010-06-01"
   tr_end = "2014-12-1"

   test_start = "2015-01-01"
   test_end = "2017-12-1"

   plt = train_test(indep_var_idx,dep_var_idx,feature_scaling,tr_start,tr_end,test_start,test_end)
   plt.show()
