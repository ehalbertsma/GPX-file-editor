'''
Created on 2019 M10 1

@author: E
'''

import trackpoint


fv = open('Morning_Run.gpx','r',encoding='utf-8')
fv2 = open('Morning_Run2.gpx','w',encoding='utf-8')

length = 12941
count=0

dlat = -(43.4897950-43.4830430) #divide by avg???
dlon = -(-80.5327620--80.5344540)

#print(dlat,dlon)


for i in range(8):
    fv2.write(fv.readline())
fv2.write("  <trkseg>\n")

trkptlist = list()
# actual points
while fv.readline():
    latlon=fv.readline().split('"') # latlon needs format
    #print(latlon)
    
    if len(latlon) < 3:
        continue
    if (count>0) and (trkptlist[-1]['time']>='    <time>2019-11-08T15:45:24Z</time>'):
        print(count)
        dlat=0
        dlon=0
    
    lat=str(float(latlon[1])+dlat)
    lon=str(float(latlon[3])+dlon)
    
    ele=fv.readline() # ele no format
    time=fv.readline() #time no format
    
    fv.readline() #nothing
    fv.readline() #nothing
    
    hr=fv.readline() #hr
    cad = fv.readline() #cad
    fv.readline() #nothing
    
    fv.readline() #nothing

    track_point = {
        'latitude': lat,
        'longitude': lon,
        'elevation': ele,
        'time': time,
        'hr': hr,
        'cad': cad
    }
    
    trkptlist.append(track_point)
    count+=1

for trkpt in trkptlist:

    fv2.write('   <trkpt lat="{}" lon="{}">\n'.format(trkpt['latitude'],trkpt['longitude']))
    fv2.write(trkpt['elevation'])
    fv2.write(trkpt['time'])
    fv2.write("    <extensions>\n")
    fv2.write("     <gpxtpx:TrackPointExtension>\n")
    fv2.write(trkpt['hr'])
    fv2.write(trkpt['cad'])
    fv2.write("     </gpxtpx:TrackPointExtension>\n")
    fv2.write("    </extensions>\n")
    fv2.write("   </trkpt>\n")
    
fv2.write("  </trkseg>\n")
fv2.write(" </trk>\n")
fv2.write("</gpx>\n")


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