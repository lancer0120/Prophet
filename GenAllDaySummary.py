#!/usr/bin/python3

import os,glob
import pandas as pd

def main():

    ## Merge database 
    aFolderPath = 'data_repository/Database/'
    
    AllSumRpts = glob.glob(aFolderPath + '*/Summary.csv')

    AllDFs = []
    for aRpt in AllSumRpts:
        print(aRpt)
        aDF = pd.read_csv(aRpt)
        AllDFs.append(aDF)

    aDF = pd.concat(AllDFs, join='inner') 

    oDF = aDF.reset_index(drop=True)

    oDF['FinalPrice'] = 'not-ready'
    oDF['Ratio']      = 'not-ready'
    oDF['Key']        = 'not-ready'

    df = pd.read_csv('./20210723.csv',header = None,encoding = 'ISO-8859-1')
    AllCodes =  list(df[0])
    AllPrices = list(df[8])
    AllStocks = dict(zip(AllCodes,AllPrices))

    for i in range(len(oDF['Stock'])):
        aStock = str(oDF['Stock'][i])
        if aStock not in AllStocks:
            continue

        oDF['FinalPrice'][i] = AllStocks[aStock]
        oDF['Ratio'][i]      = (float(oDF['FinalPrice'][i].replace(',','')) - float(oDF['Price'][i])) / float(oDF['Price'][i])
        oDF['Ratio'][i]      = '%.3f' % oDF['Ratio'][i]

        aKey = oDF['D01'][i] + oDF['D03'][i] + oDF['D05'][i] + oDF['D10'][i] + oDF['D20'][i] + oDF['D30'][i] 
        oDF['Key'][i]        = aKey

    oDF = oDF[oDF['FinalPrice'] != 'not-ready']
    oDF.to_csv('df.csv', index=False)

if __name__ == '__main__':main()

