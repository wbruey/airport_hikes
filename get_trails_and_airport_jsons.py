import unirest
import json
import csv
import math
import re

def lat_lon_conversion(old):
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



# COMMENT THIS OUT IF YOU DONT WANT TO PULL FROM API
#unirest.timeout(60)
#response = unirest.get("https://trailapi-trailapi.p.mashape.com/?lat=40.873877&limit=1000&lon=-74.279662&radius=150", headers={ "X-Mashape-Key": "k8l37AXNLImshC2h3TOTpWnW1Dhkp1tBNcRjsn6CRntn6oLBsd" })
#raw_hikes=json.loads(response.raw_body)
#with open('raw_hikes.json','wb') as outfile:
#    json.dump(raw_hikes,outfile)

# also get more hikes from the hiking project at this site
#https://www.hikingproject.com/data/get-trails?lat=42.654968&lon=-73.7559&maxDistance=70&maxResults=500&key=200403067-c85119606e5d3affb6054bcb6852fde2

########################################


with open('raw_hikes.json') as json_file:
    raw_hikes=json.load(json_file)

with open('tons_closest_hiking_project.json') as json_file:
    raw_hikes_hp=json.load(json_file)





hikes={}

hikes_found=0

for place in raw_hikes['places']:
    hikes_found=hikes_found+1
    hikes[place['name']]={}
    hikes[place['name']]['lat']=place['lat']
    hikes[place['name']]['lon']=place['lon']

for place in raw_hikes_hp['trails']:
    hikes_found=hikes_found+1
    place_name=place['name']
    place_name=re.sub(r'\W+', '', place_name)
    hikes[place_name]={}
    hikes[place_name]['lat']=place['latitude']
    hikes[place_name]['lon']=place['longitude']



print('Hikes Found:')
print(hikes_found)

airports={}

with open('north_east_airports.csv') as csvfile:
    spamreader=csv.DictReader(csvfile)
    for row in spamreader:
        if row['Type']=='AIRPORT' and row['Use']=='PU':
            airports[row['LocationID'][1:]]={}
            airports[row['LocationID'][1:]]['lat']=lat_lon_conversion(row['ARPLatitude'])
            airports[row['LocationID'][1:]]['lon']=lat_lon_conversion(row['ARPLongitude'])

with open('hikes.json','wb') as outfile:
    json.dump(hikes,outfile)

with open('airports.json','wb') as outfile:
    json.dump(airports,outfile)


