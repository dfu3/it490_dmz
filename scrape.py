import requests
import json

r = requests.get('https://openexchangerates.org/api/latest.json?app_id=0e838b78b3234442a7628ddf4b3dec90')
allData = (r.json())
rates = allData['rates']
myData = dict()

for rate in rates:
    if(rate == 'EUR'):
        myData[rate] = (rates[rate])
    elif(rate == 'USD'):
        myData[rate] = (rates[rate])
    elif(rate == 'AUD'):
        myData[rate] = (rates[rate])
    elif(rate == 'BTC'):
        myData[rate] = (rates[rate])
    elif(rate == 'CAD'):
        myData[rate] = (rates[rate])
    elif(rate == 'GBP'):
        myData[rate] = (rates[rate])
    elif(rate == 'INR'):
        myData[rate] = (rates[rate])
    elif(rate == 'JPY'):
        myData[rate] = (rates[rate])
    elif(rate == 'MXN'):
        myData[rate] = (rates[rate])
    elif(rate == 'RUB'):
        myData[rate] = (rates[rate])
    elif(rate == 'CNY'):
        myData[rate] = (rates[rate])

print((myData))
        
