
"""
ideal setup

Input:
    2 lists of trackpoints (i.e. the outputs of fileIO.import_trackpoints)
    2 data_fields
    desired splicing parameter (e.g. heart rate)
Output:
    1 list of trackpoints (that can be inputted into fileIO.export_trackpoints
    1 updated data_field for that file
Algorithm:
    1. iterate through every timestamp of trackpointlist1
    2. for each timestamp, search the second trackpointlist for that timestamp
        note: remember the current index so that you don't re-search from the top
    3. grab the desired splicing parameter and set that attribute in the trackpoint() object
        error: if that timestamp does not exist (i.e. device is paused, set the attribute as 0) to simulate sensor dropout
    4. 

"""




from ast import Return


def search_trackpointlist(trkptlist, timestamp, i=0):


    if (trkptlist[0].time['year'] != timestamp['year']) or (trkptlist[0].time['month'] != timestamp['month']):# or (trkptlist[0].time['day'] != timestamp['day']):
        raise Exception("The dates in your file do not match the timestamp.")
    
    else: 
        for trkpt in trkptlist[i:]:
            
            # consider the case where the time stamp does not exist at all
            if i==len(trkptlist)-1:
                return -1

            if trkpt.time['hour'] == timestamp['hour']:
                if trkpt.time['minute'] == timestamp['minute']:
                    if trkpt.time['second'] == timestamp['second']:
                        break
            
            i+=1

        return i

def replace_data(trkptlist1, trkptlist2):
    """
    trkptlist 1 is preserved
    we add data of field "field" (e.g., hr, cad, etc) from trkptlist2 to trkptlist1

    """
    errorcount = []
    index = 0
    for trkpt1 in trkptlist1:

        timestamp = trkpt1.time
        
        index = search_trackpointlist(trkptlist2, timestamp, index)
        if index == -1:
            trkpt1.hr = 0
            errorcount.append(timestamp)
        else:
            trkpt1.hr = trkptlist2[index].hr

    return trkptlist1, errorcount


def validate_replace_data(trkptlist1, trkptlist2):

    index_list = [None]*len(trkptlist1) # errors[i] = {1 --> there IS an error, 0 --> no error, -1 --> not found}
    errorcount = []

    for i in range(len(trkptlist1)):

        for j in range(len(trkptlist2)):

            if j == len(trkptlist2):
                print("not found")
                index_list[i] = -1
                errorcount.append(trkptlist1[i].time)

            elif trkptlist1[i].time == trkptlist2[j].time:
                if trkptlist1[i].hr == trkptlist2[j].hr:
                    print("check passed")
                    index_list[i] = 0
                else:
                    print("check failed. hr is {}, should be {}".format(trkptlist1[i].hr,trkptlist2[j].hr))
                    index_list[i] = 1

    return index_list
                
def find_gap(trkptlist, mode=0,epsilon=0.0001):
    """
    modes: 0=return timestamps, 1=return epsilon
    """

    deltamax = 0
    deltai = -1

    for i in range(len(trkptlist)-1):
        
        lat1 = trkptlist[i].latitude
        lat2 = trkptlist[i+1].latitude
        lon1 = trkptlist[i].longitude
        lon2 = trkptlist[i+1].longitude

        delta2 = (lat2-lat1)**2 + (lon2-lon1)**2
        
        if deltamax < delta2:
            deltamax = delta2
            deltai = i

    if mode==0:
        return (trkptlist[deltai].time, trkptlist[deltai+1].time)
    elif mode==1:
        return deltamax
    else:
        print("wrong mode given, choose 0 or 1")

def fix_pause(trkptlist1, trkptlist2):

    """
    trkptlist1: paused file
    trkptlist2: donor file
    future improvement: recusively apply the algorithm until the file meets a maximum epsilon
    """

    timestamps = find_gap(trkptlist1)

    startindex1 = search_trackpointlist(trkptlist1,timestamps[0])
    startindex2 = search_trackpointlist(trkptlist2,timestamps[0])
    endindex1 = search_trackpointlist(trkptlist1,timestamps[1])
    endindex2 = search_trackpointlist(trkptlist2,timestamps[1])

    print(trkptlist2[startindex2].time)
    print(trkptlist2[endindex2].time)

    trkptlist3 = trkptlist1[0:startindex1] # IF THIS DOESN'T WORK TRY COPY
    #print(trkptlist3[startindex1-2:startindex1-1])

    for i in range(startindex2,endindex2):
        trkptlist3.append(trkptlist2[i])
    for i in range(endindex1,len(trkptlist1)):
        trkptlist3.append(trkptlist1[i])

    return trkptlist3



    


