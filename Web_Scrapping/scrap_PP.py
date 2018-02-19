import pandas as pd 
import requests
from bs4 import BeautifulSoup
from dateutil import parser, rrule

url = "https://www.drikpanchang.com/tables/planetary-positions-sidereal.html?date={day}/{month}/{year}&time=12:00:00"

start_date = "2000-05-01"
end_date = "2018-02-01"
start = parser.parse(start_date)
end = parser.parse(end_date)
dates = list(rrule.rrule(rrule.DAILY, dtstart=start, until=end))

def getPlanetPosition(year,month,day):
    
    data = {}
    new_url = url.format(day=day, month=month, year=year)
    print(new_url)
    r = requests.get(new_url)
    soup=BeautifulSoup(r.content,"html.parser")
    df = pd.read_html(str(soup),flavor="bs4")
    for i in range(1,15):
        feature1 = df[2].values[i,0] + "_NL"
        feature2 = df[2].values[i,0] + "_Degree"
        data[feature1] = df[2].values[i,4]
        data[feature2] = df[2].values[i,5]
    data["Date"] = "{day}/{month}/{year}".format(day=day,month=month,year=year)
    
    return data


data = []
for i,d in enumerate(dates):
    t = getPlanetPosition(d.year,d.month,d.day)
    data.append(t)

    if(i%10 == 0):
        print("Writing ...")
        df = pd.DataFrame(data).set_index("Date")
        df.to_csv("Chennai_PP_data.csv")

df = pd.DataFrame(data).set_index("Date")
df.to_csv("Chennai_PP_data.csv")
