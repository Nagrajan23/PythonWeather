import pyowm
import requests
import json
import pymongo
import requests
import threading
import time
import os
from datetime import datetime

#Database Connection
client = pymongo.MongoClient()
db = client.weather_data #Database in MongoDB

#LOCATIONS TO TRACK
data = json.load(open('config_file.json'))
number_of_cities = len(data['locations'])
refresh_rate = data['refresh_rate']
#print("Number of Cities to scan for: " + str(number_of_cities))

clear = lambda: os.system('cls')

def weather_forecast_3hr_api(location):
	api_key = "114c1288a926175bc3b7b768387bc625"
	url_to_process = "http://api.openweathermap.org/data/2.5/forecast?q="+ location +"&appid=" + api_key
	response = requests.get(url_to_process)
	#print(response)
	return response.json()

def get_forecast_3hr():
    while(True):
        for i in range(number_of_cities):
            #print(data['locations'][i])
            temp_location = data['locations'][i][0] + "," + data['locations'][i][1]
            json_object = weather_forecast_3hr_api(temp_location)

            total_forecats = len(json_object["list"])
            #total_forecats = 1
            for loop_variable in range(total_forecats):
                temp_dict = {}

                dt = json_object["list"][loop_variable]['dt_txt']
                city = json_object["city"]['name']
                status = json_object["list"][loop_variable]['weather'][0]['main']
                temp = json_object["list"][loop_variable]['main']['temp']
                temp = temp - 273
                temp_F = round((temp * 1.8) + 32)

                temp_dict['Record_Timestamp'] = datetime.now()
                temp_dict['Forecast_Timestamp'] = dt
                temp_dict['City'] = city
                temp_dict['Status'] = status
                temp_dict['Temperature_F'] = temp_F

                #print("Time Stamp:\t\t\t\t" + json_object["list"][loop_variable]['dt_txt'])
                #print("Location:\t\t\t\t" +json_object["city"]['name'])
                #print("Weather Condition:\t\t " +json_object["list"][loop_variable]['weather'][0]['main'])
                #print("Temperature:\t\t\t" +str(json_object["list"][loop_variable]['main']['temp']))

                db_result = db.weather_forecast_3hr.insert_one(temp_dict)
            
                #ALERTS
                if(status == 'Rain' or status == 'Snow' or temp_F <= 2):
                    alert_dict = {}
                    alert_dict['Forecast_Timestamp'] = dt
                    alert_dict['City'] = city
                    alert_dict['Alert_Status'] = status
                    if(temp_F <= 2):
                        alert_dict['Temperature Status'] = 'Below 2: Freezing'
                    else:
                        alert_dict['Temperature Status'] = ' '
                    alert_dict['Temperature_F'] = temp_F
                    db_result = db.weather_alerts_3hr.insert_one(alert_dict)

            time.sleep(refresh_rate)

def display_alerts():
    #get_alerts = db.weather_alerts_3hr.find({ }).sort( { Forecast_Timestamp: -1 } ).limit(50)
    #db.weather_alerts_3hr.createIndex( { id: -1 } )
    #get_alerts = db.weather_data.weather_alerts_3hr.find().sort({ _id:-1 }).limit(50)
    get_alerts = db.weather_data.weather_alerts_3hr
    {
 sort: {
  Forecast_Timestamp: -1
 },
 limit: 50
}
    print('Forecast Time \t\tCity \tAlert Status \tBelow 2F? \tTemperature')
    for alert in get_alerts:
        print(alert['Forecast_Timestamp'],'\t',alert['City'],'\t',alert['Alert_Status'],
              '\t',alert['Temperature Status'],'\t',alert['Temperature_F'])
        #db.weather_alerts_3hr.
    input('Press Enter to Continue...')

#Define Threads
five_day_forecast_thread = threading.Thread(target = get_forecast_3hr)
#sixteen_days_forecast_thread = threading.Thread(target = sixteen_days_forecast)
#weather_maps_thread = threading.Thread(target = weather_maps)
#open_and_display_maps_thread = threading.Thread(target = open_and_display_maps)
#weather_alert_thread = threading.Thread(target = weather_alert)

while(True):
    clear()

    thread_status_5day = five_day_forecast_thread.isAlive();
    if(thread_status_5day):
        thread_status_5day_string = "Running"
    else:
        thread_status_5day_string = "NOT Running"
    print("Open Weather Map Python API Program Menu\n\n")
    print("5 day/3 hr forecast thread status: " + thread_status_5day_string)
    print("\t1. Start running this thread")
    print("\t2. Stop running this thread")
    print("\n\t3. Display Last 50 Alerts")
    print("\n\n\t5. Exit Program")
    menu_option = input("\n\nEnter your option: ")
    if(menu_option == "1"):
        five_day_forecast_thread = threading.Thread(target = get_forecast_3hr)
        five_day_forecast_thread.start()
    elif(menu_option == "2"):
        five_day_forecast_thread._delete()
    elif(menu_option == "3"):
        display_alerts()
    elif(menu_option == "5"):
        exit();

five_day_forecast_thread.start()
#sixteen_days_forecast_thread.start()
#weather_maps_thread.start()
#open_and_display_maps_thread.start()

#print("Test Hello")
owm = pyowm.OWM('114c1288a926175bc3b7b768387bc625')
#observation = owm.weather_at_place('Colombo,LK')
#w = observation.get_weather()
fc = owm.three_hours_forecast('Colombo,LK')
#fc = owm.daily_forecast('Colombo,LK')
f = fc.get_forecast()
lst = f.get_weathers()
print(lst[1])
print('--------------')
print(lst[2])
print(f.get_location())

