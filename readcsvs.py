#-*-coding:utf-8-*-
__author__ = 'hu'
import os
import csv

class readcsvs:
    '''
    this class is used to read the csv files and tranform them into ansi code.
    '''
    def __init__(self):
        '''
        this is the initial function 
        '''
        pass
        
    def GetFileNames(self, path):
        '''
        get the filename from the special folder path.
        '''
        k = os.listdir(path)
        s = list()
        for i in k:
            if os.path.isdir(path+i):
                pass        #ignore the folders
            else:
                s.append(i)
        return s
        
    def transferCSV(self, path, savedcolumns):
        '''
        read the csv file
        path is the absolutely path
        '''
        files = self.GetFileNames(path) #get the filenames
        for i in range(len(files)):
            lpath = path + files[ i ]
            fp = file(lpath, 'rb')
            reader = csv.reader(fp)
            print 'deal with file %s...'%files[i]
            self.writeCSV(reader, lpath[:-4] + '_new.csv', savedcolumns)
        print 'Done'
        
    def writeCSV(self, content, path, savedcolumns):
        '''
        write the CSV
        content is the opened csv file
        path is the absolutely path of the new file.
        header is table header ban.
        '''
        
        #open a new file to save the data.
        wfp = file(path, 'wb')
        writer = csv.writer(wfp)
        savedcolumns = savedcolumns.sort()  # sort the banner
        
        #write the content of the file.
        for line in content:
            writer.writerow([line[k].strip().decode('utf-8').encode('gb18030') for k in savedcolums])
        
        #write the end of the file
        wfp.flush()
        wfp.close()
        writer = ''
        
if __name__ == '__main__':
    s = readcsvs()
    savedcolums = [ i for i in range(18)]
    s.transferCSV('F:\\BaiduYun\\ict_workspace\\python\\csvReader\\data\\', savedcolums)