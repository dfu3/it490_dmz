import requests
import json
import MySQLdb

loadQ = ['EUR', 'USD', 'AUD', 'BTC', 'CAD', 'GBP', 'INR', 'JPY', 'MXN', 'RUB', 'CNY']
outerQ = loadQ[:]
innerQ = loadQ[:]

myDB = MySQLdb.connect(host="10.200.45.9",port=3306,user="dmz",passwd="letMe1n",db="user_info")
curs = myDB.cursor()
curs.execute("truncate exchange;")

for outerCurr in outerQ:
    allCurr = requests.get("https://openexchangerates.org/api/latest.json?app_id=0e838b78b3234442a7628ddf4b3dec90&base=" + outerCurr).json()
    allRates = allCurr['rates']
    print(innerQ)
    print('---+---+---+---+---+---+--->')
    for innerCurr in innerQ:
        if (innerCurr != outerCurr):
            print(outerCurr + ' ==> ' + innerCurr + ': ' + str(allRates[innerCurr]))
            curs.execute("insert into exchange(currency_1, currency_2, rate)  values('" + outerCurr + "', '" + innerCurr + "', '" + str(allRates[innerCurr]) + "');")
            curs.execute("insert into exchange_backup(currency_1, currency_2, rate)  values('" + outerCurr + "', '" + innerCurr + "', '" + str(allRates[innerCurr]) + "');")
    innerQ.remove(outerCurr)

myDB.commit()
