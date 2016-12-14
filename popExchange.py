import requests
import os
import json
import MySQLdb
import socket
from getLimits import getLimits

loadQ = ['EUR', 'USD', 'AUD', 'CHF', 'CAD', 'GBP', 'INR', 'JPY', 'MXN', 'RUB', 'CNY']
outerQ = loadQ[:]
innerQ = loadQ[:]

try:
    myDB = MySQLdb.connect(host="10.200.45.16",port=3306,user="dmz",passwd="letMe1n",db="user_info")

except(Exception):
    myDB = MySQLdb.connect(host="10.200.20.230",port=3306,user="dmz",passwd="letMe1n",db="user_info")

curs = myDB.cursor()
curs.execute("select grouping from exchange order by id desc limit 1;")
currGroup = curs.fetchone()[0]
currGroup = str(int(currGroup) + 1)
curs.execute("truncate exchange;")
curs.execute("truncate currencies;")
curs.execute("truncate trade_limits;")

#currGroup = 1 #uncomment if resetting 'grouping' column
print(currGroup)

allCurrDesc = requests.get("https://openexchangerates.org/api/currencies.json").json()
for curr in loadQ:
    curs.execute("insert into currencies(currency, description)  values('" + curr + "', '" + allCurrDesc[curr] + "');")

for outerCurr in outerQ:
    allCurr = requests.get("https://openexchangerates.org/api/latest.json?app_id=0e838b78b3234442a7628ddf4b3dec90&base=" + outerCurr).json()
    allRates = allCurr['rates']
    print(innerQ)
    print('---+---+---+---+---+---+--->')
    for innerCurr in innerQ:
        if (innerCurr != outerCurr):
            print(outerCurr + ' ==> ' + innerCurr + ': ' + str(allRates[innerCurr]))
            curs.execute("insert into exchange(currency_1, currency_2, rate, grouping)  values('" + outerCurr + "', '" + innerCurr + "', '" + str(allRates[innerCurr]) + "', '" + str(currGroup) + "');")
            curs.execute("insert into exchange_backup(currency_1, currency_2, rate, grouping)  values('" + outerCurr + "', '" + innerCurr + "', '" + str(allRates[innerCurr]) + "', '" + str(currGroup) + "');")

            curs.execute( "select rate from exchange_backup where (currency_1='" + outerCurr + "' and currency_2='" + innerCurr + "') or (currency_1='" + innerCurr + "' and currency_2='" + outerCurr + "') order by grouping desc limit 32;" )

            result = [item[0] for item in curs.fetchall()]
            lims = getLimits(result)

            curs.execute("insert into trade_limits(currency_1, currency_2, upper, lower, rate) values('" + outerCurr +  "', '" + innerCurr +  "', '" + str(lims[0]) + "', '" + str(lims[1]) + "', '" + str(allRates[innerCurr]) + "');")
            
    innerQ.remove(outerCurr)

myDB.commit()
