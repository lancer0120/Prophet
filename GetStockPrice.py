import requests
import pandas as pd
import numpy as np
import datetime,time
import os

def main():

    aFolderPath = 'data_repository\\StockPrice\\'
    if os.path.isdir(aFolderPath) is False:
        os.system('mkdir %s' % aFolderPath)
    

    aStartDay = datetime.date(2021,1,1)
    aOneDay   = datetime.timedelta(days=1) 
    aCheckDay = aStartDay
    aToday = datetime.datetime.now().strftime('%Y%m%d')

    while aCheckDay.strftime('%Y%m%d') != aToday:
        aCheckDay += aOneDay
        datestr   =  aCheckDay.strftime('%Y%m%d')
        print('Procssing %s ... ' % datestr)

        ofile = aFolderPath + datestr + '.csv'
        if os.path.isfile(ofile): continue

        r = requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALL')
        
        f = open(ofile,'w')
        StockData = r.text.partition('"1101"')
        f.write(StockData[1]+StockData[2].replace('\r',''))
    
        f.close()
        time.sleep(10)


if __name__ == '__main__':main()

