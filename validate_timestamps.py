"""
validate_timestamps

For a list of trackpoints, we want to see if the timestamps are in order. That means
- all points are in strictly monotonically increasing order
- there are no duplicate points
- there are no Null timestamps

"""
import fileIO

def compare_trkpt(trkptlist,verbose=False):
    count_fails = 0
    count_success = 0
    for i in range(len(trkptlist)-1):
        trkpt1 = trkptlist[i]
        trkpt2 = trkptlist[i+1]

        bool = trkpt_timecompare(trkpt1,trkpt2,verbose=verbose) # returns a true if trkpt2 > 1
        if not bool:
            count_fails+=1
            print(f"Failed at {trkpt1.disp_datetime()}.")
        else:
            count_success+=1

    print(f"Fail: {count_fails}, Success: {count_success}")
        
        

def validate_dates(trkptlist):
    year  = trkptlist[0].time['year']
    month = trkptlist[0].time['month']
    day   = trkptlist[0].time['day']

    print(f"Base timestamp: {trkptlist[0].disp_date()}")

    i = 0 # index of trkpts
    j = 0 # index of mismatches
    for trkpt in trkptlist:
        if (trkpt.time['year'] != year) or (trkpt.time['month'] != month) or (abs(trkpt.time['day'] - day) > 0):
            raise Exception(f"Date mismatch at index {i}, timestamp {trkpt.disp_time()}.")
            j+=1
        i+=1

    print(f"Found {j} mismatches.")


def trkpt_timecompare(trkpt1,trkpt2,compare_dates=False,verbose=False):
    """
    Checks if trkpt2.time > trkpt1.time
    Optional argument determines whether you also want to check the date. If you have already passed validate_dates then leave this argument false.
    """

    if compare_dates:
        if verbose: 
            print(f"Check: {trkpt2.disp_datetime()} > {trkpt1.disp_datetime()}")
        result = trkpt2.disp_datetime() > trkpt1.disp_datetime()
    else: 
        if verbose: 
            print(f"Check: {trkpt2.disp_time()} > {trkpt1.disp_time()}")
        result = trkpt2.disp_time() > trkpt1.disp_time()
    
    return result

    