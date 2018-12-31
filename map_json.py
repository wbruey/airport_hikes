import unirest
import json
import csv
import math
import os
import time

with open('airports.json') as airports_json_file:
    airports=json.load(airports_json_file)
    
with open('hikes.json') as hikes_json_file:
    hikes=json.load(hikes_json_file)


def marker_text(lat,lon,title,text):
    return '\n\rL.marker(['+str(lat)+', '+str(lon)+']).addTo(mymap).bindPopup("<b>'+str(title)+'</b><br />'+str(text)+'");\n\r'
    

def circle_text(lat,lon,title,text):
    return '\n\rL.circle(['+str(lat)+', '+str(lon)+'], 700, { color: \'red\',  fillColor: \'#f03\', fillOpacity: 0.2 }).addTo(mymap).bindPopup("<b>Hello world!</b><br />Hike Me Reb.");\n\r'

os.system('cp leaflet_map_template.html newest_map.html')
time.sleep(2)

with open("newest_map.html", "ab") as myfile:
    pass
    #myfile.write(marker_text(3,2,'hey','you'))
    #myfile.write(circle_text(1,4,'hey','you'))





    


