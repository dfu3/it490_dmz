import requests
import json
import MySQLdb
myDB = MySQLdb.connect(host="10.200.45.9",port=3306,user="dmz",passwd="letMe1n",db="user_info")
curs = myDB.cursor()

curs.execute("insert into test(testfield) values('blah_blah');")
myDB.commit()
