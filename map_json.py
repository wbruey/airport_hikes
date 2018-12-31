import unirest
import json
import csv
import math
import os
import time


def marker_text(lat,lon,title,text):
    return 'L.circle(['+str(lat)+', '+str(lon)+'], 700, { color: \'blue\',  fillColor: \'#f03\', fillOpacity: 0.2 }).addTo(mymap).bindPopup("<b>'+title+'</b><br />'+text+'");\n'

def circle_text(lat,lon,title,text):
    return 'L.circle(['+str(lat)+', '+str(lon)+'], 700, { color: \'red\',  fillColor: \'#f03\', fillOpacity: 0.2 }).addTo(mymap).bindPopup("<b>'+title+'</b><br />'+text+'");\n'

os.system('cp leaflet_map_template.html all_trips.html')
os.system('cp leaflet_map_template.html great_trips.html')
time.sleep(2)

with open('airport_hikes.json') as airports_json_file:
    airports=json.load(airports_json_file)

with open('hike_flights.json') as hikes_json_file:
    hikes=json.load(hikes_json_file)


with open("all_trips.html", "ab") as myfile:
    
    for air_key in airports:
        myfile.write(marker_text(airports[air_key]['lat'],airports[air_key]['lon'],air_key,'Closest Hike: '+airports[air_key]['closest_hike']))

    for hike_key in hikes:
        myfile.write(circle_text(hikes[hike_key]['lat'],hikes[hike_key]['lon'],hike_key,'Hike me Reb! And fly in via '+hikes[hike_key]['closest_airport']))

    myfile.write('</script> </body> </html>')





with open('great_airport_hikes.json') as airports_json_file:
    airports=json.load(airports_json_file)

with open('great_hike_flights.json') as hikes_json_file:
    hikes=json.load(hikes_json_file)


with open("great_trips.html", "ab") as myfile:

    for air_key in airports:
        myfile.write(marker_text(airports[air_key]['lat'],airports[air_key]['lon'],air_key,'Closest Hike: '+airports[air_key]['closest_hike']))

    for hike_key in hikes:
        myfile.write(circle_text(hikes[hike_key]['lat'],hikes[hike_key]['lon'],hike_key,'Hike me Reb! And fly in via '+hikes[hike_key]['closest_airport']))

    myfile.write('</script> </body> </html>')


