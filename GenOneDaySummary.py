#!/usr/bin/python3

import os,glob

def main():

    aFolderPath = 'data_repository/Database/'
    
    AllFolders = glob.glob(aFolderPath + '*')

    for aFolder in AllFolders:
        aRunDay = os.path.basename(aFolder)
        AllCSVs = glob.glob(aFolder + '/D*.csv')
        oFileName = aFolder + '/Summary.csv'

        if os.path.isfile(oFileName) is True:
            print('%s is existed, override it !!!' % oFileName)

        ofp = open(oFileName,'w')
        AllSumDB        = {}
        AllStockPrice   = {}
        AllSumItems     = []
        for aCSV in AllCSVs:
            aKey = os.path.splitext(os.path.basename(aCSV))[0]
            aSumDB = []
            
            ifp = open(aCSV,'r')
            lines = ifp.readlines()
            for line in lines:
                aline = line.strip().split(',')
                aSumDB.append(aline[0])
                AllStockPrice[aline[0]] = aline[1]
                AllSumItems.append(aline[0])
            
            AllSumDB[aKey] = aSumDB
            ifp.close()
        aTitle = 'Stock,RunDay,Price,' + ','.join(AllSumDB.keys())
        ofp.write(aTitle + '\n')
        AllSumSet = set(AllSumItems)
        for aItem in AllSumSet:
            ItemStr = aItem + ',' + aRunDay + ',' + AllStockPrice[aItem]
            for aKey in AllSumDB.keys():
                if aItem in AllSumDB[aKey]:
                    ItemStr += ',O'
                else:
                    ItemStr += ',X'
            ofp.write(ItemStr + '\n')

        ofp.close()

if __name__ == '__main__':main()

