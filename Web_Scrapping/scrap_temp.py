import pandas as pd 
import requests
from bs4 import BeautifulSoup
from dateutil import parser, rrule


url = "https://www.wunderground.com/history/airport/VOMM/{year}/{month}/{day}/DailyHistory.html?req_city=Chennai&req_state=TN&req_statename=India&reqdb.zip=00000&reqdb.magic=245&reqdb.wmo=43278"
start_date = "2000-05-01"
end_date = "2018-02-1"


start = parser.parse(start_date)
end = parser.parse(end_date)
dates = list(rrule.rrule(rrule.DAILY, dtstart=start, until=end))

def getTemp(year,month,day):
    
    data = {}
    url = "https://www.wunderground.com/history/airport/VOMM/{year}/{month}/{day}/DailyHistory.html?req_city=Chennai&req_state=TN&req_statename=India&reqdb.zip=00000&reqdb.magic=245&reqdb.wmo=43278"
    new_url = url.format(day=day, month=month, year=year)
    print(new_url)
    r = requests.get(new_url)
    soup=BeautifulSoup(r.content,"html.parser")

    data["Date"] = "{day}/{month}/{year}".format(day=day,month=month,year=year)
    try:
       df = pd.read_html(str(soup),flavor="bs4")
    except Exception as e:
       return data

   # if not "Actual" in df[0]:
    #    return data

    try:
       data["Mean Temp"] = df[0].Actual[1].replace("\xa0°C", "")
    except Exception as e:
       pass

    try: 
       data["Max Temp"] = df[0].Actual[2].replace("\xa0°C", "")
    except Exception as e:
       pass

    try:
       data["Min Temp"] = df[0].Actual[3].replace("\xa0°C", "")
    except Exception as e:
       pass

    try:
       data["Dew point (celcius)"] = df[0].Actual[7].replace("\xa0°C", "")
    except Exception as e:
       pass

    try:
       data["Avg Humidity"] = df[0].Actual[8]
    except Exception as e:
       pass

    try:
       data["Max Humidity"] = df[0].Actual[9]
    except Exception as e:
       pass

    try: 
       data["Min Humidity"] = df[0].Actual[10]
    except Exception as e:
       pass

    try:
       data["Wind Spd (Km/h)"] = df[0].Actual[16].replace("\xa0km/h  ()", "")	
    except Exception as e:
       pass

    try:
       data["Max Wind Spd (Km/h)"] = df[0].Actual[17].replace("\xa0km/h", "") 
    except Exception as e:
       pass

    try:
       data["Sea pres (hPa)"] = df[0].Actual[14].replace("\xa0hPa", "")
    except Exception as e:
       pass
    
    return data

data = []
for i,d in enumerate(dates):
    t = getTemp(d.year,d.month,d.day)
    data.append(t)

    if(i%10 == 0):
        print("Writing ...")
        df = pd.DataFrame(data).set_index("Date")
        df.to_csv("Chennai_temperature_data.csv")

df = pd.DataFrame(data).set_index("Date")
df.to_csv("Chennai_temperature_data.csv")
