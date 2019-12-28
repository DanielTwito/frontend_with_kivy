"""
This is a web Service API, that makes a recommendation
for a user who wants to go for a trip to NY City using Bike share service
"""

from flask import Flask
from flask import jsonify
from flask import request
from backend import Database

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def recommend():
    database=Database()
    loc = request.args.get('startlocation')
    time = request.args.get('timeduration')
    nor = request.args.get('k')
    ans = database.recommend(loc,time,nor)
    return  jsonify(ans)


if __name__ == '__main__':
    app.run()