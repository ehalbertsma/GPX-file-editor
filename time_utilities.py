from datetime import datetime, timezone

# class Timestamp:
#     def __init__(self, dict):
#         self.year   = dict['year']
#         self.month  = dict['month']
#         self.day    = dict['day']
#         self.hour   = dict['hour']
#         self.minute = dict['minute']
#         self.second = dict['second']

#     def disp_datetime(self):
#         return ("{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(self.year,self.month,self.day,self.hour,self.minute,self.second))
    
#     def disp_time(self):
#         return ("{:02d}:{:02d}:{:02d}".format(self.hour,self.minute,self.second))
    
#     def disp_date(self):
#         return ("{:04d}-{:02d}-{:02d}".format(self.year,self.month,self.day))


class Timestamp:
    def __init__(self, dict):
        self.timestamp = datetime(
                year   = dict['year'],
                month  = dict['month'],
                day    = dict['day'],
                hour   = dict['hour'],
                minute = dict['minute'],
                second = dict['second'] 
            )
        
    def convert_to_epoch(self):
        return int(self.timestamp.replace(tzinfo=timezone.utc).timestamp())
    
    def convert_to_iso4601(self=None, epoch_seconds=None):
        if epoch_seconds:
            return datetime.utcfromtimestamp(epoch_seconds).isoformat()
        else:
            return self.timestamp.replace().isoformat()


def convert_to_timestamp(epoch_seconds):
    return datetime.utcfromtimestamp(epoch_seconds)

def generate_timepoints(timestamp1, timestamp2, interval=1):
    """
    Returns a list of timestamps at (default 1 second) intervals between the two input timestamps

    """
    timestamp1 = Timestamp(timestamp1)
    timestamp2 = Timestamp(timestamp2)

    ts1 = timestamp1.convert_to_epoch()
    ts2 = timestamp2.convert_to_epoch()
    
    generated_timestamps = list()
    
    curr = ts1

    while curr <= ts2:
        generated_timestamps.append(Timestamp.convert_to_iso4601(epoch_seconds=curr))
        curr += interval

    return generated_timestamps


def add_dummy_times(trkptlist):
    """
    adds dummy 0000-00-00T00:00:00 timestamps to every trkpt in trkptlist
    
    """

    for trkpt in trkptlist:
        trkpt.time["year"]  = 0 
        trkpt.time["month"] = 0
        trkpt.time["day"]   = 0
        trkpt.time["hour"]  = 0
        trkpt.time["minute"] = 0
        trkpt.time["second"] = 0

    return trkptlist

def add_non_dummy_times(trkptlist, timestamplist):
    """
    adds legit YYYY-MM-DDT00:00:00 timestamps to every trkpt in trkptlist
    
    """
    length_trkptlist = len(trkptlist)
    length_timestamplist = len(timestamplist)

    if length_trkptlist < length_timestamplist:
        raise IndexError("Need at least as many GPS points as timestamps.")

    print(f"""Matching {length_timestamplist} timestamps to {length_trkptlist} GPS points.
Timestamp start: {timestamplist[0]}
Timestamp end:   {timestamplist[length_trkptlist]}          
""")

    for i in range(length_trkptlist):

        dates = timestamplist[i].split("T")[0].split("-")
        times = timestamplist[i].split("T")[1].split(":")

        trkptlist[i].time["year"]  = int(dates[0])
        trkptlist[i].time["month"] = int(dates[1])
        trkptlist[i].time["day"]   = int(dates[2])
        trkptlist[i].time["hour"]  = int(times[0])
        trkptlist[i].time["minute"] = int(times[1])
        trkptlist[i].time["second"] = int(times[2])

    return trkptlist