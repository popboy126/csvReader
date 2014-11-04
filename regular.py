#-*-coding:utf-8-*-
#this script is used to find the special string in the string
__author__ = 'hucheng'
import re
class MyReg:
    '''
    my regular express
    '''
    def __init__(self):
        '''
        do some initial things
        rule=r'http://[a-zA-Z0-9./]*'
        '''
        #self.rule = re.compile(rule)    #get the rule

    def OmitTheStr(self, rule, substr ,s):
        '''
        omit the string in the string such as the URL
        '''
        return re.sub(rule, substr, s)

    def match(self, rule, content):
        '''
        match the whole content if it is suit for the rule
        '''
        return re.match(rule, content)