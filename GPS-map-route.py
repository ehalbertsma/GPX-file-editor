'''
Created on 2020 TR3 9

@author: Emrys

IN: a gpx activity and a gpx map
OUT: a gpx activity with the route approximation overlaid with the time

- convert both input files to trackpoints to extract data
- map each trackpoint from the time activity to the best fit trackpoint from the map file
    complications:
        - there are more points in the map file than then time file
        - how to deal with pauses?
'''

#import trackpoint
# import xmltodict
import sys
from math import sqrt


#input gpx activity with messy gps
fv_time = open('workingDir/finn_time1.gpx','r',encoding='utf-8')
#input gpx route file
fv_map = open('workingDir/finn1_map1.gpx','r',encoding='utf-8')
#output gpx activity
fv_out = open('outputDir/new file.gpx','w',encoding='utf-8')   


# Imported File Fields
flags_map = {
    "eleflag": True,
    "hrflag": False,
    "timeflag": False,
    "cadflag": False,
    "pwrflag": False
}
flags_time = {
    "eleflag": True,
    "hrflag": True,
    "timeflag": True,
    "cadflag": False,
    "pwrflag": False
}

def norm(trkpt1, trkpt2):
    lat1, lon1 = trkpt1['latitude'], trkpt1['longitude']
    lat2, lon2 = trkpt2['latitude'], trkpt2['longitude']
    # print(lat1,lat2,lon1,lon2)

    return sqrt( (lat2 - lat1)**2 + (lon2 - lon1)**2 )


# header for the exported file
for i in range(8):
    fv_out.write(fv_time.readline())
    #fv_time.readline()
fv_out.write("  <trkseg>\n")

# line = fv.readline()
# #fv2.write(line)
# while line != "  <trkseg>\n":
#     print(line)
#     line = fv.readline()
#     #fv2.write(line)
# #fv2.write(fv.readline())

def importData(fv, flags):
    
    if not(flags["timeflag"]): # if it's a map gpx file, there's a bunch of junk at the top of the file we want to skip
        for i in range(18):
            print(fv.readline())


    trkptlist = list()
    
    while fv.readline():
        """
        Here we add the cleaned trackpoint data into a list called trkptlist.
        Note that only the latitude and longitude data is scrubbed - the rest we can simply keep in string format since we only care about chaning latitude and longitude.
        """
        line = fv.readline()

        # check for end of file
        if line == '  </trkseg>\n':
            break 

        latlon = line.split('"') # latlon needs float conversion as we want to modify it
        # print(latlon)
        
        lat = float(latlon[1])
        lon = float(latlon[3])
        
        if flags["eleflag"]:
            ele = fv.readline() # elevation needs no float conversion as we keep it the same in the output file
        
        if flags["timeflag"]:
            time = fv.readline() # time needs no float conversion as we keep it the same in the output file
        
            fv.readline() # <extensions>
            fv.readline() #  <gpxtpx:TrackPointExtension>
        
        if flags["hrflag"]:
            hr=fv.readline() # hr
        if flags["cadflag"]:
            cad = fv.readline() # cad
        if flags["pwrflag"]:
            pwr = fv.readline() # power
        
        if flags["timeflag"]:
            fv.readline() #  </gpxtpx:TrackPointExtension>
            fv.readline() # </extensions>
        
        # fv.readline() # </trkpt>

        # now create a dictionary to store the data of each trackpoint
        track_point = {
            'latitude': lat,
            'longitude': lon,
            'elevation': ele if flags["eleflag"] else None,
            'time': time if flags["timeflag"] else None,
            'hr': hr if flags["hrflag"] else None,
            'cad': cad if flags["cadflag"] else None,
            'pwr': pwr if flags["pwrflag"] else None
        }
        
        trkptlist.append(track_point)

    return trkptlist
    


trkptlist_map = importData(fv_map,flags_map)
trkptlist_time = importData(fv_time,flags_time)

for i in range(100):#len(trkptlist_map)):
    d = norm(trkptlist_time[i],trkptlist_map[i])
    print(trkptlist_time[i]['latitude'],trkptlist_map[i]['latitude'],"\n")
    #fv_out.write("{},{}\n".format(i,d))

fv_map.close()
fv_time.close()
fv_out.close()

sys.exit()





##########################
"""
spikeindex = list()
epsilon = 2.5e-4

for i in range(len(trkptlist)-1):
    currentnorm = norm( trkptlist[i],trkptlist[i+1] )
    if currentnorm > epsilon:
        print(currentnorm)
        spikeindex.append(i)
    if currentnorm < epsilon:

        fv2.write('   <trkpt lat="{}" lon="{}">\n'.format(trkptlist[i]['latitude'],trkptlist[i]['longitude']))
        if eleflag:
            fv2.write(trkptlist[i]['elevation'])
        fv2.write(trkptlist[i]['time'])
        fv2.write("    <extensions>\n")
        fv2.write("     <gpxtpx:TrackPointExtension>\n")
        if hrflag:
            fv2.write(trkpt['hr'])
        if cadflag:
            fv2.write(trkptlist[i]['cad'])
        if pwrflag:
            fv2.write(trkptlist[i]['pwr'])
        fv2.write("     </gpxtpx:TrackPointExtension>\n")
        fv2.write("    </extensions>\n")
        fv2.write("   </trkpt>\n")
        i+=1
    
fv2.write("  </trkseg>\n")
fv2.write(" </trk>\n")
fv2.write("</gpx>\n")

print(spikeindex)

fv2.close()
fv.close()

# calc the diff in lat/long btw 15:45:24 and 15:45:24
#up until 15:45:24, we take the lat and long and add the difference

# find all the trkpts and put em in a list
"""
# for trkpt in List:
#     if time<'14:45:24':
#         lat = lat+dlat
#         long = lon+dlon

# print the list out to a new text file
"""


'  <trkpt lat='+lat+' lon='+lon+'>'
'    <ele>'+ele+'</ele>'
'    <time>2019-11-08T'+time+'Z</time>'
'    <extensions>'
'     <gpxtpx:TrackPointExtension>'
'      <gpxtpx:hr>'+hr+'</gpxtpx:hr>'
'      <gpxtpx:cad>'+cad+'</gpxtpx:cad>'
'     </gpxtpx:TrackPointExtension>'
'    </extensions>'
'   </trkpt>'
"""
