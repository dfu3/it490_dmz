import requests
import json
import MySQLdb

loadQ = ['EUR', 'USD', 'AUD', 'CHF', 'CAD', 'GBP', 'INR', 'JPY', 'MXN', 'RUB', 'CNY']
outerQ = loadQ[:]
innerQ = loadQ[:]

myDB = MySQLdb.connect(host="10.200.173.26",port=3306,user="dmz",passwd="letMe1n",db="user_info")
curs = myDB.cursor()
qOut = str(curs.execute("select grouping from exchange order by id desc limit 1;"))
currGroup = qOut[qOut.find("'")+1:1]
currGroup = str(int(currGroup) + 1)
curs.execute("truncate exchange;")
curs.execute("truncate currencies;")
#currGroup = 1 #uncomment if resetting
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
    innerQ.remove(outerCurr)

myDB.commit()
