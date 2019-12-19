import sqlite3
import pandas as pd
import os

class Database():
    def __init__(self):
        files = os.listdir("./")
        if "database.db" in files:
            self.conn = sqlite3.connect("database.db")
            return
        else:
            data = pd.read_csv("BikeShare.csv")
            self.conn=sqlite3.connect("database.db")
            data.to_sql("BikesInfo_tbl",self.conn,if_exists="replace")


d=Database()
