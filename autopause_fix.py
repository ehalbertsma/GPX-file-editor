
from copy import copy
import fileIO
import splice_files as sf

# Imported File Fields
# --------------------

# enter name and directory of input file
input_filename1  = 'workingDir/heidi.gpx'
input_filename2  = 'workingDir/The_Presidential_Traverse.gpx'

output_filename1 = 'outputDir/heidi_fixed.gpx'

# select data fields to import
data_flags1 = {
    'gpsflag':  True,
    'timeflag': True,
    'eleflag':  True,
    'hrflag':   False, 
    'cadflag':  True, 
    'pwrflag':  False 
}
data_flags2 = {
    'gpsflag':  True,
    'timeflag': True,
    'eleflag':  True,
    'hrflag':   True, 
    'cadflag':  True, 
    'pwrflag':  False 
}
data_flags3 = {
    'gpsflag':  True,
    'timeflag': True,
    'eleflag':  True,
    'hrflag':   False, 
    'cadflag':  False, 
    'pwrflag':  False 
}

trkptlist1, meta_data1 = fileIO.import_trackpoints(data_flags1, input_filename1)
trkptlist2, meta_data2 = fileIO.import_trackpoints(data_flags2, input_filename2)

trkptlist3 = sf.fix_pause(trkptlist1,trkptlist2)

fileIO.export_trackpoints(data_flags3,trkptlist3,meta_data1,output_filename1)
