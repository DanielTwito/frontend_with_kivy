"""
this code is for pre-processing
on the data in this script we query the data base and search
for 3 closest neighbors for each Stat station
this information is save in csv file to help us in the recommendation algorithm.
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


def get_loc():
    d=Database()
    col_name = [
                "StartStationName",
                "StartStationLatitude",
                "StartStationLongitude"]
    cur = d.conn.cursor()
    li1 = cur.execute("""SELECT DISTINCT StartStationName,StartStationLatitude,StartStationLongitude FROM BikesInfo_tbl""")\
                        .fetchall()
    res = pd.DataFrame(li1, columns=col_name)
    loc = {}
    for i, row in res.iterrows():
        index = row["StartStationName"]
        x=row["StartStationLatitude"]
        y=row["StartStationLongitude"]
        loc[index] = Point(float(x),float(y))
    loc_neighbor={}
    for i in loc:
        loc_neighbor[i]=get_neighbor((i, loc[i]), loc)
        # break
    return loc_neighbor

def get_neighbor(curr, loc):
    n={}
    for key in loc:
        if curr[0] == key:
            continue
        n[key]=curr[1].get_distance(loc[key])
    sorted_n = list(map(lambda t:t[0],sorted(n.items(), key=lambda kv: kv[1])))[:3]
    return sorted_n


d=get_loc()
lbl=d.keys()
df=pd.DataFrame(d,columns=lbl)
df.to_csv("loc_neighbor.csv")
