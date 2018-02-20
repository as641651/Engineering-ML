import pandas as pd
from dateutil import parser, rrule
import numpy as np

start_date = "2000-06-01"
end_date = "2000-08-1"

def getDegrees_Y(dates_string,temperatures,planet_data,y_index=6):

   arr_idx =  [np.where(temperatures.values[:,0] == d)[0][0] for d in dates_string]

   Y=[]
   for i in arr_idx:
       try:
         if not np.isnan(float(temperatures.iloc[i,y_index])):
           Y.append([i, temperatures.iloc[i,0], float(temperatures.iloc[i,y_index])])
       except ValueError:
         pass

   Y = np.array(Y)
   Y_keys = ["id","Date",temperatures.keys()[y_index]]

   arr_idx2 =  [np.where(planet_data.values[:,0] == d)[0][0] for d in Y[:,1]]
   X_keys = planet_data.iloc[:,1::2].keys()
   X = planet_data.values[arr_idx2][:,1::2]

   assert(len(X)==len(Y))
   return {"X_keys" : X_keys, "X" : X, "Y_keys" : Y_keys, "Y":Y}

def getDateString(start_date,end_date):
   start = parser.parse(start_date)
   end = parser.parse(end_date)
   dates = list(rrule.rrule(rrule.DAILY, dtstart=start, until=end))
 
   dates_string = ["{day}/{month}/{year}".format(day=d.day,month=d.month,year=d.year) for d in dates]

   return dates_string

if __name__ == '__main__':

    #start = parser.parse(start_date)
    #end = parser.parse(end_date)
    #dates = list(rrule.rrule(rrule.DAILY, dtstart=start, until=end))
 
    #dates_string = ["{day}/{month}/{year}".format(day=d.day,month=d.month,year=d.year) for d in dates]

    temperatures = pd.read_csv("Chennai_temperature_data.csv")
    Y_keys = temperatures.keys()
    #print(Y_keys)
    planet_data = pd.read_csv("Chennai_PP_data.csv")

    dates_string = getDateString(start_date,end_date)
    ret = getDegrees_Y(dates_string,temperatures,planet_data,6)
    print(ret)
    print(len(ret["X"]),len(ret["Y"]))
