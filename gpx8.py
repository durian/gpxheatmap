import gpxpy
import gpxpy.gpx
from math import sqrt
from math import radians, cos, sin, asin, sqrt
import sys
import pandas as pd
import folium
from folium import plugins

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

#gpx_file = open( '2017-01-05_13-03-11.gpx', 'r' )
#gpx_file = open( '2017-04-06_11-26-02.gpx', 'r')
#gpx_file = open( 'merged.gpx', 'r')
#gpx_file = open( 'CONC_20170701_20170731.GPX', 'r')

max_points = 400000
skip = 2

latlons = []
sum_lat = 0
sum_lon = 0
num = 0
parsed = 0
skipped = 0
import os

fn_gpx = "1967_Tracks.gpx"
if os.path.isfile(fn_gpx) and fn_gpx.endswith("gpx"):
    print( fn_gpx )
    f = open(fn_gpx, 'r')
    try:
        gpx = gpxpy.parse(f)
    except:
        print( "ERROR PARSING FILE" )
        skipped += 1
        sys.exit(1)
        #gpx = gpxpy.parse(fn) #the above works better, opening file first
    parsed += 1
    for track in gpx.tracks:
        tnum = 0
        for segment in track.segments:
            #print( "SEGMENT", len( segment.points ) )
            for point in segment.points:
                if tnum % skip == 0:
                    latlons.append([ point.latitude, point.longitude ]) 
                    sum_lat += point.latitude
                    sum_lon += point.longitude
                    num += 1
                tnum += 1

    #for waypoint in gpx.waypoints:
    #    print( 'waypoint {0} -> ({1},{2})'.format( waypoint.name, waypoint.latitude, waypoint.longitude ) )

    #for route in gpx.routes:
    #    print( 'Route:' )
    #    for point in route:
    #        print( 'Point at ({0},{1}) -> {2}'.format( point.latitude, point.longitude, point.elevation ) )
    print( "  POINTS", len(latlons) )
    
# There are more utility methods and functions...

# You can manipulate/add/remove tracks, segments, points, waypoints and routes and
# get the GPX XML file from the resulting object:

#print( 'GPX:', gpx.to_xml() )

print( "parsed", parsed )
print( "skipped", skipped )

ave_lat = 56.24 #sum_lat / num
ave_lon = 13.24 #sum_lon / num

#https://python-graph-gallery.com/288-map-background-with-folium/
# tiles='CartoDB dark_matter',
#folium.TileLayer('mapquestopen').add_to(my_map) (https://deparkes.co.uk/2016/06/10/folium-map-tiles/)
m = folium.Map([ave_lat, ave_lon], zoom_start=11,
               #tiles='Stamen Terrain'
)
#folium.TileLayer('Stamen Terrain').add_to(m) 


# Maybe plot only 1%, or  250000 points..
print( "latlons", len(latlons) )

import random
random.shuffle( latlons )

sparse_latlons = latlons[0:max_points]
print( "sparse_latlons", len(sparse_latlons) )
# maybe add more than one heatmap? Per year?
m.add_child(plugins.HeatMap(sparse_latlons, radius=8) ) #, gradient={.4: 'blue', .65: 'lime', 1: 'red'}))   

#folium.PolyLine( sparse_latlons ).add_to(m)

m.save("gpx8.html")              
print( "saved gpx8.html" )

'''

...
2018/2018-01-25_17-29-48.gpx
  POINTS 4973323

real	14m38.777s
user	14m28.942s
sys	0m4.790s


2018/2018-01-25_17-29-48.gpx
  POINTS 998094
parsed 2997
skipped 9
div 3
sparse_latlons 332698
saved gpx5.html

real	15m9.254s
user	15m4.976s
sys	0m2.772s

'''
