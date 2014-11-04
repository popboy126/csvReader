#-*-coding:utf-8-*-
__author__ = 'hu'
import os
import csv
import cPickle

class ReadFolder:
    '''
    read the file in the folder
    '''
    def __init__(self):
        '''
        do some initial things
        '''
        self.header = [ '消息ID', '用户ID', '消息内容', '转发数', '评论数' ]
        self.fileOrder = 0
        self.filepath = 'd:\\mobile\\mobile'
        self.allitems = 5000
        self.curItems = 0
        self.wfp = ''
        self.writer = ''

    def writeCSV(self, docid, content,  topic, flag):
        '''
        write the CSV
        '''
        if flag == 1:
            self.wfp.flush()
            self.wfp.close()
            self.curItems = 0
            self.writer = ''
        else:
            for line in content:
                if self.wfp == '':
                    self.wfp = file(self.filepath + str(self.fileOrder) + '.csv', 'wb')
                    self.fileOrder += 1
                    self.writer = csv.writer(self.wfp)
                    self.writer.writerow(self.header)

                s = line[6]#.decode('utf-8').encode('gb18030')
                if topic in s:
                    self.writer.writerow([ docid, line[0], line[6], line[12], line[13]])
                    self.curItems += 1

                if self.curItems == self.allitems:
                    self.wfp.flush()
                    self.wfp.close()
                    self.wfp = ''
                    self.curItems = 0


    def GetFileNames(self, path):
        '''
        because this is a demo. so it will ignore the folders
        '''
        k = os.listdir(path)
        s = list()
        for i in k:
            if os.path.isdir(path+i):
                pass        #ignore the folders
            else:
                s.append(i)
        return s

    def readFolderFiles(self, path):
        '''
        read the files under the path folder
        '''
        files = self.GetFileNames(path) #get the filenames
        context=list()
        for i in range(len(files)):
            s = open(path + files[i], 'rb')
            l = s.read()
            s.close()
            context.append([i, l])
        return {'names': files, 'context': context}

    def readCSV(self, path, topic):
        '''
        read the csv file
        path is the absolutely path
        '''
        files = self.GetFileNames(path) #get the filenames
        for i in range(len(files)):
            fp = file(path + files[ i ] , 'rb')
            reader = csv.reader(fp)
            print 'deal with file %s...'%files[i]
            self.writeCSV(i, reader, topic,0)

        self.writeCSV( 0, 0, 0, 1)     #flush
        k = cPickle.dumps(files, True)
        avf = open('d:\\mobile\\files.txt', 'wb')
        avf.write(k)
        avf.flush()
        avf.close()
        print 'Done'

        #return reader

    def OmitRepeat(self, path):
        '''
        Omit the repeat messages
        '''
        files = self.GetFileNames(path) #get the filenames
        for i in range(len(files)):
            fp = file(path + files[ i ] , 'rb')
            reader = csv.reader(fp)
            content = list()
            print 'deal with file %s...'%files[i]
            for line in reader:
                if content:
                    if content[ -1 ] == line:
                        continue
                content.append(line)
            fp.close()
            fp = file(path + files[ i ] , 'wb')
            writer = csv.writer(fp)
            writer.writerows(content)
            fp.flush()
            fp.close()

if __name__ == '__main__':
    c = ReadFolder()
    #s ='手机'
    #c.readCSV('I:\\2012-08-14\\', s)
    c.OmitRepeat('data/mobile/')



