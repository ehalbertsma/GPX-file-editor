"""
Functions for working with the GPS lat/lon pairs

"""
from math import radians, sin, cos, sqrt, atan2
from fileIO import TrackPoint
from numpy import linspace

def haversine(trkpt1, trkpt2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [trkpt1.latitude, trkpt1.longitude, trkpt2.latitude, trkpt2.longitude])

    # Calculate the differences between latitudes and longitudes
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1)*cos(lat2)*sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Calculate the distance
    distance = R*c*1000

    return distance


def calculate_norm2(trkpt1, trkpt2):
    """ 
    norm squared of the difference between GPS coordinates. 
    Warning! This is the norm squared and NOT the norm. This is done for ease of computing.
    """
    lat1 = trkpt1.latitude
    lat2 = trkpt2.latitude
    lon1 = trkpt1.longitude
    lon2 = trkpt2.longitude

    return (lat2-lat1)**2 + (lon2-lon1)**2 

def find_gap(trkptlist, mode=0,epsilon=0.0001):
    """
    Traverses the entire trkptlist and returns output corresponding to the trkpt with the largest GPS coordinate difference between itself and the previous coordinate
    modes: 0=return epsilon, 1=return timestamps, 2=return two lists containing lat/lon coords of the 2 points
    """

    deltamax =  0 # variable storing the largest gap between gps points so far in the trkptlist
    deltai   = -1 # variable storing the index in trkptlist of the point with the largest gap

    for i in range(len(trkptlist)-1):
        
        delta2 = calculate_norm2(trkptlist[i],trkptlist[i+1])
        
        if deltamax < delta2:
            deltamax = delta2
            deltai = i

    deltai += 1 # grab the point after the gap??

    if mode==0:
        return deltamax
    elif mode==1:
        return (trkptlist[deltai].disp_datetime(), trkptlist[deltai+1].disp_datetime())
    if mode==2:
        return (trkptlist[deltai].latitude, trkptlist[deltai].longitude), (trkptlist[deltai+1].latitude, trkptlist[deltai+1].longitude)
    else:
        print("wrong mode given, choose {0,1,2}")

def find_closest(trkpt1,trkptlist):
    """
    Given a trkpt list (as generated in fileIO.py), and a pair of arbitrary coordinates, find the closest point in the trkptlist to the pair of coordinates.
    The "closest" point is defined as the one which minimizes the output of calculate_norm2.
    Returns the index of trkptlist corresponding to that minimum.
    """
    deltamin = 1
    deltamin_index = -1

    print(f"Finding closest point to:  ({trkpt1.latitude},{trkpt1.longitude})...")

    for i in range(len(trkptlist)):

        delta = calculate_norm2(trkpt1,trkptlist[i])
        if delta < deltamin:
            deltamin = delta
            deltamin_index = i
    
    print(f"Closest point in the list: ({trkptlist[deltamin_index].latitude},{trkptlist[deltamin_index].longitude}) at index={deltamin_index}")

    return deltamin_index

def compute_total_distance(trkptlist,haversine_dist=True):
    """
    Computes the total distance of the route

    """
    distance = 0

    for i in range(len(trkptlist)-1):

        a = trkptlist[i]
        b = trkptlist[i+1]

        a_to_b = haversine(a,b) if haversine_dist else sqrt(calculate_norm2(a,b))

        distance += a_to_b
    
    return distance

def fraction_of_total_distance(trkptlist):
    """
    Outputs a list. The i^th element of the list describes the unitless distance from trkptlist[i-1] to trkptlist[i]
    """

    total_distance = compute_total_distance(trkptlist,haversine_dist=False)

    distances_by_node = list() # each element corresponds to the segment of the route (between 2 tkrpts) that matches the indices of trkptlist
    distances_by_node.append(0)

    for i in range(1, len(trkptlist)):

        a = trkptlist[i-1]
        b = trkptlist[i]

        a_to_b = sqrt(calculate_norm2(a,b))

        distances_by_node.append(a_to_b/total_distance)
    
    return distances_by_node


def distance_per_segment(trkptlist):
    """
    Outputs a list. The i^th element of the list describes the unitless distance from trkptlist[i-1] to trkptlist[i]
    """

    distances_by_node = list() # each element corresponds to the segment of the route (between 2 tkrpts) that matches the indices of trkptlist
    distances_by_node.append(0)

    for i in range(1, len(trkptlist)):

        a = trkptlist[i-1]
        b = trkptlist[i]

        distances_by_node.append(haversine(a,b))
    
    return distances_by_node

def add_interpolated_points(trkptlist2, data_flags, N):
    """
    Outputs the exact same GPS track but with N interpolated points.
    """
    fracs = fraction_of_total_distance(trkptlist2)
    add_points = [round(N*i) for i in fracs]


    original_length = len(trkptlist2)
    trkptlist2_dense = list()

    for i in range(1, original_length):
        
        if add_points[i] > 1:

            new_lats = linspace(trkptlist2[i-1].latitude, trkptlist2[i].latitude, add_points[i])
            new_lons = linspace(trkptlist2[i-1].longitude, trkptlist2[i].longitude, add_points[i])
            if data_flags['eleflag']:
                new_eles = linspace(trkptlist2[i-1].elevation, trkptlist2[i].elevation, add_points[i])
            if data_flags['hrflag']:
                new_hrs = linspace(trkptlist2[i-1].hr, trkptlist2[i].hr, add_points[i])
            if data_flags['cadflag']:
                new_cads = linspace(trkptlist2[i-1].cad, trkptlist2[i].cad, add_points[i])
            if data_flags['pwrflag']:
                new_pwrs = linspace(trkptlist2[i-1].pwr, trkptlist2[i].pwr, add_points[i])

            # densified_segment = list()
            for j in range(add_points[i]):
                new_trkpt = TrackPoint()

                new_trkpt.latitude = new_lats[j]
                new_trkpt.longitude = new_lons[j]
                if data_flags['eleflag']:
                    new_trkpt.elevation = new_eles[j]
                if data_flags['hrflag']:
                    new_trkpt.hr = new_hrs[j]
                if data_flags['cadflag']:
                    new_trkpt.cad = new_cads[j]
                if data_flags['pwrflag']:
                    new_trkpt.pwr = new_pwrs[j]

                trkptlist2_dense.append(new_trkpt)

        elif add_points[i] == 1:
            trkptlist2_dense.append(trkptlist2[i])

    print(f"Original number of points: {original_length}, new number of points: {len(trkptlist2_dense)}.")
    print(f"Original distance: {compute_total_distance(trkptlist2)}, new distance: {compute_total_distance(trkptlist2_dense)}.")

    return trkptlist2_dense