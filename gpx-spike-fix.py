'''
Created on 2020 M12 27

@author: E
'''

# import xmltodict
import sys
from math import sqrt

# Imported File Fields
filename = 'workingDir/Night_run.gpx' # name of file
eleflag, hrflag, cadflag, pwrflag = True, False, False, False


fv = open(filename,'r',encoding='utf-8')
fv2 = open('outputDir/Run2.gpx','w',encoding='utf-8')

def norm(trkpt1, trkpt2):
    lat1, lon1 = trkpt1['latitude'], trkpt1['longitude']
    lat2, lon2 = trkpt2['latitude'], trkpt2['longitude']
    # print(lat1,lat2,lon1,lon2)

    return sqrt( (lat2 - lat1)**2 + (lon2 - lon1)**2 )


for i in range(8):
    fv2.write(fv.readline())
fv2.write("  <trkseg>\n")

# line = fv.readline()
# #fv2.write(line)
# while line != "  <trkseg>\n":
#     print(line)
#     line = fv.readline()
#     #fv2.write(line)
# #fv2.write(fv.readline())


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

    latlon = line.split('"') # latlon needs format
    print(latlon)
    
    
    lat = float(latlon[1])
    lon = float(latlon[3])
    
    if eleflag:
        ele = fv.readline() # elevation no format

    time = fv.readline() # time no format
    fv.readline() # <extensions>
    fv.readline() #  <gpxtpx:TrackPointExtension>
    
    if hrflag:
        hr=fv.readline() # hr
    if cadflag:
        cad = fv.readline() # cad
    if pwrflag:
        pwr = fv.readline() # power
    
    
    fv.readline() #  </gpxtpx:TrackPointExtension>
    fv.readline() # </extensions>
    # fv.readline() # </trkpt>

    # now create a dictionary to store the data of each trackpoint
    track_point = {
        'latitude': lat,
        'longitude': lon,
        'elevation': ele if eleflag else None,
        'time': time,
        'hr': hr if hrflag else None,
        'cad': cad if cadflag else None,
        'pwr': pwr if pwrflag else None
    }
    
    trkptlist.append(track_point)
    

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
for trkpt in List:
    if time<'14:45:24':
        lat = lat+dlat
        long = lon+dlon

# print the list out to a new text file



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
