
import fileIO
import splice_files as sf

# Imported File Fields
# --------------------

# enter name and directory of input file
input_filename1  = 'workingDir/30_mar_zwift_gps.gpx'
input_filename2  = 'workingDir/30_mar_zwift_hr.gpx'

output_filename1 = 'outputDir/out.gpx'
output_filename2 = 'outputDir/out2.gpx'
# select data fields to import
data_flags1 = {
    'gpsflag':  True,
    'timeflag': True,
    'eleflag':  True,
    'hrflag':   False, 
    'cadflag':  True, 
    'pwrflag':  True 
}
data_flags2 = {
    'gpsflag':  False,
    'timeflag': True,
    'eleflag':  False,
    'hrflag':   True, 
    'cadflag':  False, 
    'pwrflag':  False 
}

trkptlist1, meta_data1 = fileIO.import_trackpoints(data_flags1, input_filename1)
trkptlist2, meta_data2 = fileIO.import_trackpoints(data_flags2, input_filename2)

#trkptlist1[100].get_trackpoint()
#trkptlist2[100].get_trackpoint()

#timestamp = trkptlist2[100].get_time()

#index = sf.search_trackpointlist(trkptlist1, timestamp)
#print(index)

trkptlist3, errorcount = sf.replace_data(trkptlist1, trkptlist2)

data_flags3 = data_flags1
data_flags3['hrflag'] = True

print(len(errorcount))

fileIO.export_trackpoints(data_flags1, trkptlist1, meta_data1, output_filename1)
fileIO.export_trackpoints(data_flags3, trkptlist3, meta_data1, output_filename2)

