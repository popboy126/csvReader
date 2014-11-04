#-*-coding:utf-8-*-
__author__ = 'hu'
#the data Node
import cPickle
from FileOperation import myFileOperation
from VSM import VSM
import csv
from math import log

class SubDataNode:
    '''
    the sub data node
    '''
    def __init__(self):
        '''
        do some initial things
        '''
        self.all = 0    #the key appear times
        #[document id, message id, appear time]
        self.val = list()   #the data


class DataNode:
    '''
    store the information about the microblog
    '''
    def __init__(self):
        '''
        do some initial things
        '''
        self.All = 0 #the number of all microblog
        self.tKeys = list() #store the list of the key value
        #{key:[ all, [[document id, message id, appear time],] ]}
        self.tKeysAll = '' #store the whole appear times
        self.keyMatrix = dict()     #the key Matrix
        self.tKeyslen = 0   #the length of tKeys
        self.matchThreshold = 0.3

    def AddtKeys(self, key):
        '''
        Add the keys
        '''
        for i in key:
            if i not in self.tKeys:
                self.tKeys.append( i )

    def SavetKeys(self, path = 'keys/'):
        '''
        save the keys
        '''
        s = cPickle.dumps([ self.All, self.tKeys], True)
        avl = open(path + 'keys', 'wb')
        avl.write(s)
        avl.flush()
        avl.close()
        print 'write keys done...'

        avl = open(path + 'keys.txt', 'wb')
        s = 'All microblog %d\r\n'%self.All
        print s
        s += '\r\n'.join(self.tKeys)
        s = s.encode('gb18030')
        avl.write(s)
        avl.flush()
        avl.close()
        print 'write keys.txt done...'

    def LoadtKeys(self, path = 'keys/keys', flag = 0):
        '''
        Load tKeys
        '''
        mf = myFileOperation()
        self.All, self.tKeys = mf.LoadsObject(path)   #get the keys.
        self.initialMatrix(flag)

    def initialMatrix(self, flag):
        '''
        initial something
        '''
        self.tKeyslen = len( self.tKeys )
        if not flag:
            self.tKeysAll = [0 for i in range( self.tKeyslen )]
        else:
            self.LoadPartial('keys/keysPartial')

    def transform(self, codetype):
        '''
        transform the tKeys into proper coding
        '''
        for i in range(self.tKeyslen):
            self.tKeys[ i ] = self.tKeys[ i ].encode(codetype)

    def AddItemsStatistics(self,  orderId, content):
        '''
        get the statistics of the items
        '''
        for i in range(self.tKeyslen):
            k = content.count( self.tKeys[ i ] )
            if k:
                self.tKeysAll[ i ] += k     #all information
                if self.keyMatrix.has_key(self.tKeys[ i ]):
                    self.keyMatrix[ self.tKeys[ i ] ].append( [ orderId, k ] )
                else:
                    self.keyMatrix[ self.tKeys[ i ] ] = [ [orderId, k] ]


    def StoreKeysAndMatrix(self, path = 'keys/keysMatrix'):
        '''
        store the keys and the matrix
        '''
        mf = myFileOperation()
        mf.DumpsObject([ self.tKeysAll, self.keyMatrix ], path)
        print 'Store tKeysAll and KeyMatrix done'

    def StorePartial(self, all, path = 'keys/keysPartial'):
        '''
        store partial result
        '''
        mf = myFileOperation()
        mf.DumpsObject([ all, self.tKeysAll, self.keyMatrix ], path)
        print 'Partial store is done!'

    def LoadPartial(self, path = 'keys/keysPartial'):
        '''
        load the partial result
        '''
        mf = myFileOperation()
        self.All, self.tKeysAll, self.keyMatrix = mf.LoadsObject(path)
        #self.tKeyslen = len(self.tKeysAll)
        print 'Load Partial store is done!'
        print self.All, self.tKeyslen
        print len(self.keyMatrix)

    def GetFeatures(self, threshold):
        '''
        get the features.
        '''
        keys = list()
        keysAll = list()
        keyMat = dict()
        for i in range(self.tKeyslen):
            if self.tKeysAll[ i ] > threshold:
                #keys[ self.tKeys[ i ] ] = self.tKeysAll[ i ]
                keys.append( self.tKeys[ i ] )
                keysAll.append( self.tKeysAll[ i ] )
                keyMat[ self.tKeys[ i ] ] = self.keyMatrix[ self.tKeys[ i ] ]
        print 'Generate Features done!!'
        return keys, keysAll, keyMat

    def GenerateFirstTopics(self, threshold = 2, flag = 1):
        '''
        Generate the first topics
        '''
        vsm = VSM()
        self.LoadtKeys(flag = 1)
        self.transform('utf-8') #coding transform
        l = self.GetFeatures(threshold)
        if not flag:
            s = vsm.GenerateTopic(l[ 0 ], l[ 1 ], l[ 2 ], self.All)
        else:#load the store data
            mf = myFileOperation()
            s = mf.LoadsObject('keys/topics')
        return l, s

    def GetSecondTopics(self, keys,  keysAll, keyMat, OneTopic):
        '''
        get second topics
        '''
        vsm = VSM()
        l = vsm.GenerateTwoTopics(keys, keysAll, keyMat, self.All, OneTopic)
        print 'Second Clustering is done!!'
        return l

    def SaveKeyswords(self, keys, object):
        '''
        print out the details of the objects
        '''
        k = object.keys()
        k.sort()
        s = ''
        for i in k:
            s += (str(i)+':\r\n')
            for j in range(len(object[ i ][ 2 ])):
                if object[ i ][ 2 ][ j ] != 0:
                    s += (keys[ j ] + '\t')
            s += '\r\n\r\n'
        mf = myFileOperation()
        mf.WriteFile(s, 'keys/classify.txt')

    def MatchResult(self, keys, keysAll, detail, fullpath, filenum):
        '''
        match the result with the classification
        '''
        wp = file('keys/result.csv', 'wb')
        writer = csv.writer(wp)
        writer.writerow(['话题分类', '消息ID', '特征', '原消息内容'])
        vsm = VSM()
        keyslent = len(keys)
        seKeys = detail.keys()#the database
        ol = 0
        zeroVector = [0 for i in range(keyslent)]
        for fileid in range(1,filenum):
            fp = file(fullpath+str(fileid)+'.csv', 'rb')
            reader = csv.reader(fp)
            for line in reader:
                if ol % 5 == 0:
                    print '%d microblog is done...'%ol
                vector = [0 for i in range(keyslent)]
                stemp = line[2]#.encode('utf-8').encode('gb18030')
                if stemp == '消息内容':
                    continue
                s = ''
                flag = 0
                for i in range(keyslent):
                    vector[ i ] = stemp.count( keys[ i ] )
                    if vector[ i ] != 0:
                        s += (';' + keys[ i ])
                    vector[ i ] = vector[ i ] * log( float(self.All+1) / (keysAll[ i ] + vector[ i ]))
                if vector == zeroVector:
                    writer.writerow(['New', line[1], s, stemp])
                    continue

                for j in range(len(seKeys)):
                    simi = vsm.CalcSim(vector, detail[ seKeys[ j ]][2])
                    if simi > self.matchThreshold:  #match success
                        writer.writerow([seKeys[ j ], line[1], s, stemp])
                        flag = 1
                        break
                if not flag:
                    writer.writerow(['New', line[1], s, stemp])
                ol += 1
            fp.close()
            wp.flush()
        #wp.flush()
        wp.close()



if __name__ == '__main__':
    c = DataNode()
    #l, s = c.GenerateFirstTopics(0, 0)
    l, s = c.GenerateFirstTopics()
    #detail = c.GetSecondTopics(l[0], l[1], l[2], s)
    mf = myFileOperation()
    #mf.DumpsObject(detail, 'keys/detail')
    mf.DumpsObject({'keys': l[0], 'keysAll': l[1]}, 'keys/keys_keysAll')
    detail = mf.LoadsObject('keys/detail')
    #c.SaveKeyswords(l[0], detail)
    c.MatchResult(l[0], l[ 1 ], detail, 'data/mobile/mobile', 343)


