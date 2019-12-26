import sqlite3
import pandas as pd
import os

class Database():
    def __init__(self):
        files = os.listdir("./")
        if "database.db" in files:
            self.conn = sqlite3.connect("database.db")
        else:
            data = pd.read_csv("BikeShare.csv")
            self.conn=sqlite3.connect("database.db")
            data.to_sql("BikesInfo_tbl",self.conn,if_exists="replace")
        self.loclist=self.get_locations()

    """
    this function extract all the location from the start ans end location
    and make a set from them
    """
    def get_locations(self):
        cur = self.conn.cursor()
        li1= cur.execute("""
                        SELECT DISTINCT StartStationName  FROM BikesInfo_tbl
                        """).fetchall()
        li2= cur.execute("""
                        SELECT DISTINCT EndStationName  FROM BikesInfo_tbl
                        """).fetchall()
        li1=[t[0].lower() for t in li1 ]
        li2=[t[0].lower() for t in li2 ]
        union =  list(set(li1) | set(li2))
        return union

    """
    check if a given location is exist inside of a distinct location list
    that we build in the constructor
    """
    def is_location_exist(self,loc):
        ans = loc.lower() in self.loclist
        return ans

    def recommand(self, loc,time,nor):
        col_name=["index",
                  "TripDuration",
                  "StartTime",
                  "StopTime",
                  "StartStationID",
                  "StartStationName",
                  "StartStationLatitude",
                  "StartStationLongitude",
                  "EndStationID",
                  "EndStationName",
                  "EndStationLatitude",
                  "EndStationLongitude",
                  "BikeID",
                  "UserType",
                  "BirthYear",
                  "Gender",
                  "TripDurationinmin"]
        low=int(time)-30
        high=int(time)+30
        cur = self.conn.cursor()
        li1 = cur.execute("""
                            SELECT * FROM BikesInfo_tbl
                            WHERE StartStationName =? AND 
                            TripDuration Between ? AND ?""",(loc,low,high)
                          ).fetchall()
        res = pd.DataFrame(li1,columns=col_name)
        popularity={}
        for i, row in res.iterrows():
            index = row["EndStationName"]
            if index in popularity:
                popularity[index]+=1
            else:
                popularity[index]=1
        print(popularity)
