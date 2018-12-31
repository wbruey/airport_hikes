import unirest
import json
import csv
import math
import numpy

def conversion(old):
    direction = {'N':1, 'S':-1, 'E': 1, 'W':-1}
    new = old.replace('-',' ')
    new = new[:-1]+' '+new[-1]
    new = new.split()
    new_dir = new.pop()
    new.extend([0,0,0])
    return (float(new[0])+float(new[1])/60.0+float(new[2])/3600.0) * direction[new_dir]

class Haversine:
    '''
    use the haversine class to calculate the distance between
    two lon/lat coordnate pairs.
    output distance available in kilometers, meters, miles, and feet.
    example usage: Haversine([lon1,lat1],[lon2,lat2]).feet

    '''
    def __init__(self,coord1,coord2):
        lon1,lat1=coord1
        lon2,lat2=coord2

        R=6371000                               # radius of Earth in meters
        phi_1=math.radians(lat1)
        phi_2=math.radians(lat2)

        delta_phi=math.radians(lat2-lat1)
        delta_lambda=math.radians(lon2-lon1)

        a=math.sin(delta_phi/2.0)**2+\
           math.cos(phi_1)*math.cos(phi_2)*\
           math.sin(delta_lambda/2.0)**2
        c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))

        self.meters=R*c                         # output distance in meters
        self.km=self.meters/1000.0              # output distance in kilometers
        self.miles=self.meters*0.000621371      # output distance in miles
        self.feet=self.miles*5280               # output distance in feet

with open('airports.json') as airports_json_file:
    airports=json.load(airports_json_file)
    
with open('hikes.json') as hikes_json_file:
    hikes=json.load(hikes_json_file)


for air_key in airports:
    airports[air_key]['distance_to_hike']=99999
    airports[air_key]['closest_hike']='none'
    airports[air_key]['hike_lat']=0
    airports[air_key]['hike_lon']=0
    for hike_key in hikes:
        distance_to_hike=Haversine([float(airports[air_key]['lon']),float(airports[air_key]['lat'])],[float(hikes[hike_key]['lon']),float(hikes[hike_key]['lat'])]).miles
        if distance_to_hike < airports[air_key]['distance_to_hike'] :
            airports[air_key]['distance_to_hike']=distance_to_hike
            airports[air_key]['closest_hike']=hike_key
            airports[air_key]['hike_lat']=hikes[hike_key]['lat']
            airports[air_key]['hike_lon']=hikes[hike_key]['lon']

for hike_key in hikes:
    hikes[hike_key]['distance_to_airport']=99999
    hikes[hike_key]['closest_airport']='none'
    hikes[hike_key]['airport_lat']=0
    hikes[hike_key]['airport_lon']=0
    for air_key in airports:
        distance_to_airport=Haversine([float(airports[air_key]['lon']),float(airports[air_key]['lat'])],[float(hikes[hike_key]['lon']),float(hikes[hike_key]['lat'])]).miles
        if distance_to_airport < hikes[hike_key]['distance_to_airport'] :
            hikes[hike_key]['distance_to_airport']=distance_to_airport
            hikes[hike_key]['closest_airport']=air_key
            hikes[hike_key]['airport_lat']=airports[air_key]['lat']
            hikes[hike_key]['airport_lon']=airports[air_key]['lon']


with open('airport_hikes.json','wb') as outfile:
    json.dump(airports,outfile)

with open('hike_flights.json','wb') as outfile:
    json.dump(hikes,outfile)


#now find the closest hikes and airports.
distances_list=[]
airports_list=[]
hikes_list=[]
for air_key in airports:
    airports_list.append(air_key)
    distances_list.append(float(airports[air_key]['distance_to_hike']))
    hikes_list.append(airports[air_key]['closest_hike'])

closest_hikes=numpy.argsort(distances_list)
great_trips={}
great_airports={}
great_hikes={}
for i in range(50):
    distance=distances_list[closest_hikes[i]]
    airport=airports_list[closest_hikes[i]]
    hike=hikes_list[closest_hikes[i]]
    great_trips[i]={}
    great_trips[i]['airport']=airport
    great_trips[i]['distance']=distance
    great_trips[i]['hike']=hike
    great_airports[airport]=airports[airport]
    great_hikes[hike]=hikes[hike]

with open('great_trips.json','wb') as outfile:
    json.dump(great_trips,outfile)

with open('great_airport_hikes.json','wb') as outfile:
    json.dump(great_airports,outfile)

with open('great_hike_flights.json','wb') as outfile:
    json.dump(great_hikes,outfile)

