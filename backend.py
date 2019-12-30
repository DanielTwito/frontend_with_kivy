import sqlite3
import pandas as pd
import os

class Database():
    """
    we decided to use to_sql function in pandas for database creation after
    we saw it's more efficient by far than loop over the data frame and make insert query
    every iteration
    """
    def __init__(self):
        files = os.listdir("./")
        if "database.db" in files:
            self.conn = sqlite3.connect("database.db")
        else:
            data = pd.read_csv("BikeShare.csv")
            self.conn=sqlite3.connect("database.db")
            # cur = self.conn.cursor()
            # cur.execute(
            #     """CREATE TABLE BikesInfo_tbl(TripDuration INTEGER,
            #                                   StartTime TEXT,
            #                                   StopTime TEXT,
            #                                   StartStationID INTEGER,
            #                                   StartStationName TEXT,
            #                                   StartStationLatitude REAL,
            #                                   StartStationLongitude REAL,
            #                                   EndStationID INTEGER,
            #                                   EndStationName TEXT,
            #                                   EndStationLatitude REAL,
            #                                   EndStationLongitude REAL,
            #                                   BikeID INTEGER,
            #                                   UserType TEXT,
            #                                   BirthYear INTEGER,
            #                                   Gender INTEGER,
            #                                   TripDurationinmin INTEGER);""")
            # self.insert_data_to_database(data,cur)
            data.to_sql("BikesInfo_tbl",self.conn,if_exists="replace")
        self.loclist=self.get_locations()


    def insert_data_to_database(self, data,cur):
        for i, row in data.iterrows():
            cur.execute("INSERT INTO BikesInfo_tbl VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",\
                 (row["TripDuration"], row["StartTime"], row["StopTime"],row["StartStationID"],
                  row["StartStationName"],row["StartStationLatitude"],row["StartStationLongitude"],
                  row["EndStationID"],row["EndStationName"],row["EndStationLatitude"],row["EndStationLongitude"],
                  row["BikeID"],row["UserType"],row["BirthYear"],row["Gender"],row["TripDurationinmin"]))



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

    def recommend(self, loc, time, nor):
        """
        this function makes a recommendation for the user based on the location,duration time
        :param loc: current location of the user
        :param time: duration time the user want to spent
        :param nor: number of recommendation the user want to get
        :return: list of location
        """
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
        low=int(time)
        high=int(time)
        cur = self.conn.cursor()
        df= pd.read_csv("loc_neighbor.csv")
        tmp = loc
        loc = df[loc].tolist()
        loc.append(tmp)
        sql = """
                            SELECT * FROM BikesInfo_tbl
                            WHERE StartStationName = '%s' OR StartStationName = '%s' OR StartStationName = '%s' OR StartStationName = '%s'  AND 
                            TripDurationinmin Between %d AND %d """%(loc[0],loc[1],loc[2],loc[3],low-2,high+2)
        li1 = cur.execute(sql).fetchall()
        res = pd.DataFrame(li1,columns=col_name)
        popularity={}
        for i, row in res.iterrows():
            index = row["EndStationName"]
            if index in popularity:
                popularity[index]+=1
            else:
                popularity[index]=1
        sorted_p = list(map(lambda t: t[0], sorted(popularity.items(), key=lambda kv: kv[1],reverse=True)))
        ans = sorted_p[:min(int(nor),len(sorted_p))]
        print(ans)
        return ans

