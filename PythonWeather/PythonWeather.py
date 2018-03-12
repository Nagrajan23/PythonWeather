import pyowm

#print("Test Hello")
owm = pyowm.OWM('114c1288a926175bc3b7b768387bc625')
#observation = owm.weather_at_place('Colombo,LK')
#w = observation.get_weather()
fc = owm.three_hours_forecast('Colombo,LK')
f = fc.get_forecast()
lst = f.get_weathers()
print(lst[1])
print('--------------')
print(lst[2])
print(f.get_location())
