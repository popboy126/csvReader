#-*-coding:utf-8-*-
#file operation
__author__ = 'hucheng'
import cPickle

class myFileOperation:
    '''
    do some file operations
    '''
    def __init__(self):
        '''
        some initial process
        '''
        pass

    def DumpsObject(self, content, fullpath):
        '''
        store the objects
        '''
        fp = open(fullpath, 'wb')
        fp.write(cPickle.dumps(content, True))
        fp.flush()
        fp.close()

    def LoadsObject(self, fullpath):
        '''
        load Object
        '''
        fp = open(fullpath, 'rb')
        s = fp.read()
        fp.close()
        return cPickle.loads(s)

    def WriteFile(self, content, fullpath):
        '''
        write file
        '''
        fp = open(fullpath, 'wb')
        fp.write(content)
        fp.flush()
        fp.close()

    def ReadFile(self, fullpath):
        '''
        read file
        '''
        fp = open(fullpath, 'rb')
        s = fp.read()
        fp.close()
        return s
