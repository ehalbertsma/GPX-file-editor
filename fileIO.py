'''
Created on 2020 M12 27

@author: Emrys Halbertsma

Future features to add:
    - auto detect data fields
'''
import sys
import re
from math import sqrt

# now create a dictionary to store the data of each trackpoint
class TrackPoint:
    def __init__(self):
        self.latitude = None
        self.longitude = None
        self.elevation = None
        self.time = {
            'year': None,
            'month': None,
            'day': None,
            'hour': None,
            'minute': None,
            'second': None
        }
        self.hr = None
        self.cad = None
        self.pwr = None

    def get_coordinates(self):
        return list(self.latitude, self.longitude)

    def get_time(self):
        return self.time
    
    def disp_datetime(self):
        return ("{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(self.time["year"],self.time["month"],self.time["day"],self.time["hour"],self.time["minute"],self.time["second"]))
    
    def disp_time(self):
        return ("{:02d}:{:02d}:{:02d}".format(self.time["hour"],self.time["minute"],self.time["second"]))
    
    def disp_date(self):
        return ("{:04d}-{:02d}-{:02d}".format(self.time["year"],self.time["month"],self.time["day"]))


    def __str__(self):
        return f"({self.latitude}, {self.longitude}), {self.disp_datetime()}"
    # end class
#-------------------------------------

def import_trackpoints(data_flags, input_filename, skip_metadata=True):
    """
        import_trackpoints 
        receives
            two filenames in the directory
        outputs
            dictionary list of trackpoints
            metadata list of metadata that comes at the top of the gpx file

    """
    trkpt_count = 0 # counter variable which increments for every trkpt added to trkptlist
    ele_broken_count = 0 # counter variable for my file with broken elevation

    fv = open(input_filename,'r',encoding='utf-8')

    # regex stuff that will help us extract numbers from the data
    numeric_const_pattern = '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
    rx = re.compile(numeric_const_pattern, re.VERBOSE)

    trkptlist = list()
    meta_data = {
        'device': None,
        'time': None,
        'activity name': None,
        'activity type': None,
    }

    if not skip_metadata:
        # get through all the meta spam
        fv.readline()
        meta_data['device'] = fv.readline().split('"')[1]
        fv.readline()
        time = fv.readline()
        
        time = rx.findall(time)
        meta_data['time'] = {
            'year': int(time[0]),
            'month': -1*int(time[1]),
            'day': -1*int(time[2]),
            'hour': int(time[3]),
            'minute': int(time[4]),
            'second': int(time[5]),
        }
        fv.readline()
        fv.readline()
        meta_data['activity name'] = fv.readline()[8:-8]
        meta_data['activity type'] = fv.readline()[8:-8]

        print(meta_data)
    
    elif skip_metadata:
        line = fv.readline()
        while line.strip() !=  "<trkseg>":
            line = fv.readline()
    
    while line.strip() != '</trkseg>':
        """
        Here we add the parsed trackpoint data into a list called trkptlist.
        
        """
        # define new trackpoint object
        trackpoint = TrackPoint()
        
        # extract GPS coordinates
        if data_flags['gpsflag']:
            line = fv.readline()
            
            if line.strip() != '</trkseg>':
                
                latlon = line.split('"') # latitude/longitude data needs to be formatted
                trackpoint.latitude = float(latlon[1])
                trackpoint.longitude = float(latlon[3])
            
            else:
                break
        
        # extract elevation
        ele_broken = False
        if data_flags['eleflag']:
            ele = fv.readline() # elevation no format
            
            if "<ele>" in ele:
                trackpoint.elevation = float(rx.findall(ele)[0])
            else:
                trackpoint.elevation = trkptlist[-1].elevation
                ele_broken = True
                ele_broken_count +=1
            

        # extract time
        if data_flags['timeflag']:
            # time = fv.readline() # time no format
            time = ele if ele_broken else fv.readline() # time no format

            
            time = rx.findall(time)
            
            trackpoint.time = {
                'year': int(time[0]),
                'month': -1*int(time[1]),
                'day': -1*int(time[2]),
                'hour': int(time[3]),
                'minute': int(time[4]),
                'second': int(time[5]),
            }
            

            # skip some spam lines
            fv.readline() # <extensions>
        
        # extract power data
        if data_flags['pwrflag']:
            pwr = fv.readline() # power
            trackpoint.pwr = int(rx.findall(pwr)[0])

        if data_flags['timeflag']: # this line seems to be only needed for time-based gpx files
            fv.readline() #  <gpxtpx:TrackPointExtension>

        # extract HR
        if data_flags['hrflag']:
            hr=fv.readline() # hr
            hr = int(rx.findall(hr)[0]) if len(rx.findall(hr))>0 else 0
            trackpoint.hr = hr

        # extract cadence
        if data_flags['cadflag']:
            cad = fv.readline() # cad
            trackpoint.cad = int(rx.findall(cad)[0])

        # print(f"""{trkpt_count}
        # lat    {trackpoint.latitude}
        # lon    {trackpoint.longitude} 
        # ele    {trackpoint.elevation} (broken: {ele_broken_count})
        # time   {trackpoint.get_time}
        # hr     {trackpoint.hr}
        # """)


        if data_flags['timeflag']: # this line seems to be only needed for time-based gpx files
            # skip more spam
            fv.readline() #  </gpxtpx:TrackPointExtension>
            fv.readline() # </extensions>
        
        fv.readline() # </trkpt>

        # add this trackpoint to the list of all trackpoints in the GPX file
        trkptlist.append(trackpoint)
        trkpt_count +=1

    fv.close()
    print(f"{trkpt_count} points imported from {input_filename}.")
    return trkptlist, meta_data


def export_trackpoints(data_flags, trkptlist, output_filename, meta_data=None):
    """
    export_trackpoints 
        inputs
            
        outputs       

    """

    print("Exporting file...")

    fv = open(output_filename,'w',encoding='utf-8')

    if meta_data:
        # write metadata top section
        fv.write("""<?xml version="1.0" encoding="UTF-8"?>
<gpx creator="{}" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd" version="1.1" xmlns="http://www.topografix.com/GPX/1/1" xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1" xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3">
<metadata>
<time>{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z</time>
</metadata>
<trk>
<name>{}</name>
<type>{}</type>
<trkseg>\n""".format(\
        meta_data['device'],
        meta_data['time']['year'],
        meta_data['time']['month'],
        meta_data['time']['day'],
        meta_data['time']['hour'],
        meta_data['time']['minute'],
        meta_data['time']['second'],
        meta_data['activity name'],
        meta_data['activity type']))

    else:
        fv.write("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" creator="Suunto app" version="1.1" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd">
<metadata>
    <name>suuntoapp-Running-2023-12-21T11-26-59Z</name>
    <desc/>
    <author>
      <name>emrys</name>
    </author>
</metadata>
  <trk>
    <name>suuntoapp-Running-2023-12-21T11-26-59Z</name>
    <type>running</type>
    <trkseg>\n""")

    for trkpt in trkptlist:
        
        # GPS INFO ---------------------------------
        if data_flags['gpsflag']:
            #    <trkpt lat="44.4939710" lon="-80.2437380">
            # formats the GPS coordinate info
            lat,lon = trkpt.latitude,trkpt.longitude
            gpscoords =   ' lat="{:.7f}" lon="{:.7f}"'.format(lat,lon)

        fv.write('   <trkpt{}>\n'.format(gpscoords))
        # -------------------------------------------

        # Elevation INFO ----------------------------
        if data_flags['eleflag']:
            fv.write('    <ele>{:.1f}</ele>\n'.format(trkpt.elevation))
        # -------------------------------------------

        # Time INFO ---------------------------------
        if data_flags['timeflag']:
            fv.write("    <time>{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z</time>\n".format(\
      trkpt.time['year'],
      trkpt.time['month'],
      trkpt.time['day'],
      trkpt.time['hour'],
      trkpt.time['minute'],
      trkpt.time['second']))
        # -------------------------------------------

        fv.write('    <extensions>\n')
        
        # Power INFO --------------------------------
        if data_flags['pwrflag']:
            fv.write('     <power>{}</power>\n'.format(trkpt.pwr))
        # -------------------------------------------
        
        fv.write('     <gpxtpx:TrackPointExtension>\n')

        # Heart rate INFO ---------------------------
        if data_flags['hrflag']:
            fv.write('      <gpxtpx:hr>{}</gpxtpx:hr>\n'.format(trkpt.hr))
        # -------------------------------------------
           
        # Cadence INFO ---------------------------
        if data_flags['cadflag']:
            fv.write('      <gpxtpx:cad>{}</gpxtpx:cad>\n'.format(trkpt.cad))
        # -------------------------------------------
            
        fv.write('     </gpxtpx:TrackPointExtension>\n')
        fv.write('    </extensions>\n')
        fv.write('   </trkpt>\n')


    fv.write("""  </trkseg>
 </trk>
</gpx>\n""")

    fv.close()

    print("File exported to {}".format(output_filename))