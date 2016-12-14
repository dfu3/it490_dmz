import requests
import json
import MySQLdb


def split_list(alist, parts=1):
    length = len(alist)
    return [ alist[i*length // parts: (i+1)*length // parts]
             for i in range(parts) ]

def getLimits(hist):#gets upper nd lower bounds for when to trade security

    rateArr = split_list(hist, parts=3)
    upperList = list()
    lowerList = list()
    
    for subArr in rateArr:
        upperList.append(max(subArr))
        lowerList.append(min(subArr))

    uppSum = 0
    for rate in upperList:
        uppSum+= float(rate)
    lowSum = 0
    for rate in lowerList:
        lowSum+= float(rate)
        
    upperLim = uppSum/float(len(upperList))
    lowerLim = lowSum/float(len(lowerList))
    
    return (upperLim, lowerLim)

'''
FOR TESTING ALG
***************
myDB = MySQLdb.connect(host="10.200.173.68",port=3306,user="dmz",passwd="letMe1n",db="user_info")
curs = myDB.cursor()

curr1 = 'USD'
curr2 = 'EUR'
curs.execute( "select rate from exchange_backup where (currency_1='" + curr1 + "' and currency_2='" + curr2 + "') or (currency_1='" + curr2 + "' and currency_2='" + curr1 + "') order by grouping desc limit 20;" )

result = [item[0] for item in curs.fetchall()]
print('Ex. Rates for '  + curr1 + '/' + curr2)  

for rate in result:
    print(rate)

lims = getLimits(result)
print('upper limit: ' + str(lims[0]))
print('lower limit: ' + str(lims[1]))

myDB.commit()
'''