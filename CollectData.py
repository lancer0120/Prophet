from bs4 import BeautifulSoup
import requests
import re,os,datetime

def main():

    AllJobs = {'D1': 'https://concords.moneydj.com/z/zk/zk1/zkparse_420_1.djhtm',
               'D3': 'https://concords.moneydj.com/z/zk/zk1/zkparse_420_3.djhtm',
               'D5': 'https://concords.moneydj.com/z/zk/zk1/zkparse_420_5.djhtm',
               'D10':'https://concords.moneydj.com/z/zk/zk1/zkparse_420_10.djhtm',
               'D20':'https://concords.moneydj.com/z/zk/zk1/zkparse_420_20.djhtm',
               'D30':'https://concords.moneydj.com/z/zk/zk1/zkparse_420_30.djhtm'}

    res = requests.get(AllJobs['D1'])
    bs = BeautifulSoup(res.text,'html.parser')

    aRawWebDate = bs.find('div', {'class':'zkf0'} ).string.split(':')[1]
    aWebDateArray = aRawWebDate.split('/')
    aWebDate = '%02d%02d' % (int(aWebDateArray[0]),int(aWebDateArray[1]))


    aToday = datetime.datetime.now().strftime('%Y%m%d')
    aCheckToday = datetime.datetime.now().strftime('%m%d')
    if aWebDate != aCheckToday:
        print('Web is not ready: WebDate(%s) != Today(%s), ' % (aWebDate,aCheckToday))
        return

    aFolderPath = 'data_repository\\Database\\' + aToday
    if os.path.isdir(aFolderPath) is True:
        print('Job is already done: %s' % aFolderPath)
        return
    
    os.system('mkdir %s' % aFolderPath)
        
    aMatcher = re.compile('^[0-9]+')

    for aKey in AllJobs.keys():
        aWebAddress = AllJobs[aKey]
        res = requests.get(aWebAddress)
        bs = BeautifulSoup(res.text,'html.parser')

        aTable = bs.find('table')
        #aTableDate = aTable[2].findAll('tr')[1].findAll('td')[0]
        
        #return

        
        ResArray = []
        for row in aTable.findAll('tr'):
            Cells = row.findAll('td')
            if len(Cells) != 5: continue 

            aList    = []
            for aCell in Cells:
                aString = aCell.string
                if aString is None:
                    aString = aCell.find('a').string
                aList.append(aString)
            ResArray.append(aList) 

        aDumpFile = aFolderPath + '\\' + aKey +  '.csv'
        f = open(aDumpFile,'w')
        for i in range(1,len(ResArray)):
            Items = ResArray[i]
            m = aMatcher.search(Items[0])
            if m:
                Items[0] = m.group(0)
            
            aDumpStr = ','.join(Items)
            f.write(aDumpStr + '\n')

        
        f.close()
    #aTags = bs.find_all('a')
    #for tag in aTags:
    #    print(tag.string)

if __name__ == '__main__':main()
