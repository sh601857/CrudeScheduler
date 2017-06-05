#coding=utf-8 

import configparser
from pathlib import Path
import LogWidget

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

#Python2
#class MyClass(BaseClass):
#    __metaclass__ = Singleton

#Python3
class AppProject(metaclass=Singleton):
    def __init__(self):
        #super(AppProject, self).__init__() 
        self.mConfig = configparser.ConfigParser() 
        self.reset()     
        self.mLogWdg = None

    def reset(self):
        self.mFilePath = u''
        self.mConfig['Paths'] = {'Excel': 'Excel', 'gms': 'gms',
                          'Sol': 'Sol'}        
               
    def save(self):
        if self.mFilePath !='' and Path( self.mFilePath ).parent.exists():          
            with open(self.mFilePath, 'w') as projectfile:
                self.mConfig.write(projectfile)

    def load(self):
        if self.mFilePath !='' and  Path( self.mFilePath ).exists():
            self.mConfig.clear()
            self.mConfig.read(self.mFilePath)
            
    def creatFolder(self):
        profile = Path( self.mFilePath )
        if self.mFilePath !='' and  profile.exists():
            for key in self.mConfig['Paths'] :            
                dirPath = (profile.parent / self.mConfig['Paths'][key])
                if not dirPath.exists() :
                    dirPath.mkdir()

    def getPath(self,pathType,dfFileName):
        profile = Path( self.mFilePath )
        if self.mFilePath !='' and  profile.exists():
            if pathType in self.mConfig['Paths']:
                return str( profile.parent / self.mConfig['Paths'][pathType] / dfFileName )
        else:
            return ''
        
