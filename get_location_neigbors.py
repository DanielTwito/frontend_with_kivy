"""
This code is for pre-processing
on the data.
In this Script, we query the database and search
for 3 closest neighbors for each Stat station
this information is saved in the CSV file to help us in the recommendation algorithm.
"""

from backend import Database
import pandas as pd
import math

class Point():

    def __init__(self,x,y):
        self.x = x
        self.y = y
    def get_distance(self,other_point):
        return math.sqrt( ( (self.x-other_point.x) ** 2 ) +( (self.y-other_point.y) ** 2 )  )

    def __repr__(self) -> str:
        return "( "+str(self.x)+", "+str(self.y)+" )"


def get_location():
    """
    This function returns a dictionary with key as location and value as a list of its 3 closest
    neighbors
    :return: dictionary {key=location: value = [3 closest neighbors]
    """
    database=Database()
    col_name = [
                "StartStationName",
                "StartStationLatitude",
                "StartStationLongitude"]
    cursor = database.conn.cursor()
    query_result = cursor.execute("""SELECT DISTINCT StartStationName,StartStationLatitude,StartStationLongitude FROM BikesInfo_tbl""")\
                        .fetchall()
    result = pd.DataFrame(query_result, columns=col_name)
    locations = {}
    for location, row in result.iterrows():
        start_location = row["StartStationName"]
        latitude=row["StartStationLatitude"]
        longtitude=row["StartStationLongitude"]
        locations[start_location] = Point(float(latitude),float(longtitude))
    location_neighbor={}
    for location in locations:
        location_neighbor[location]=get_neighbor((location, locations[location]), locations)
    return location_neighbor

def get_neighbor(current_location, locations):
    """
    Get a current location and calculate the distance
    between all the other locations and return a list of the 3 closest location
    :param current_location: given location
    :param locations: all the locations and its geo-location data
    :return:
    """
    neighbors={}
    for location in locations:
        if current_location[0] == location:
            continue
        neighbors[location]=current_location[1].get_distance(locations[location])
    sorted_n = list(map(lambda t:t[0], sorted(neighbors.items(), key=lambda kv: kv[1])))[:3]
    return sorted_n


d=get_location()
lbl=d.keys()
df=pd.DataFrame(d,columns=lbl)
df.to_csv("loc_neighbor.csv")
