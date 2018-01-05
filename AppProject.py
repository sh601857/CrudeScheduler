#coding=utf-8

import sys, os
import configparser
from pathlib import Path
import shutil
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
        else:
            return  
        appCon = AppConfig()
        #copy dat files
        dst = self.getPath('Excel','CrudeScheduler.xlsm')
        src = '{0}\\dat\\CrudeScheduler.xlsm'.format( appCon.mbundle_dir )
        shutil.copyfile(src, dst)
        
        gmsfiles = ['CrudeSchMOS_CZ_Data.gms','CrudeSchMOS_CZ_RunOP.gms','CrudeSchMOS_CZ_SolveN.gms','CrudeScheMOS_CZ_PostSolve.gms','cplex.opt','gms.gpr','aclear.bat','MaximalClique.py']
        for gmsf in gmsfiles:
            dst = self.getPath('gms',gmsf)
            src = '{1}\\dat\\{0}'.format(gmsf,appCon.mbundle_dir)
            shutil.copyfile(src, dst)
        
    def getPath(self,pathType,dfFileName):
        profile = Path( self.mFilePath )
        if self.mFilePath !='' and  profile.exists():
            if pathType in self.mConfig['Paths']:
                return str( profile.parent / self.mConfig['Paths'][pathType] / dfFileName )
        else:
            return ''
               
class AppConfig(metaclass=Singleton):
    def __init__(self):
        #super(AppProject, self).__init__() 
        self.mConfig = configparser.ConfigParser() 
        self.reset() 
        if getattr(sys, 'frozen', False):
            # we are running in a bundle
            self.mbundle_dir = sys._MEIPASS
        else:
            # we are running in a normal Python environment
            self.mbundle_dir = os.path.dirname(os.path.abspath(__file__))        
        
    def reset(self):
        self.mConfig['Paths'] = {'gams': 'C:\\GAMS\\win64\\24.7\\gams.exe', 'dat': 'dat'
                                } 
        self.mConfig['Recent'] = {'1':'','2':'','3':'','4':'','5':''}
    
    def load(self):
        if Path( '{0}\\CrudeScheduler.config'.format(self.mbundle_dir) ).exists():
            #self.reset()
            self.mConfig.read('{0}\\CrudeScheduler.config'.format(self.mbundle_dir)) 
        else:
            print('[{0}\\CrudeScheduler.config] is missing.'.format(self.mbundle_dir))
            
    def save(self):          
        with open('{0}\\CrudeScheduler.config'.format(self.mbundle_dir), 'w') as confile:
            self.mConfig.write(confile)    
    
    def pushRecent(self,recentFile):
        for N in range(1,6,1):
            if self.mConfig['Recent']['{0}'.format(N)] == recentFile:
                break
        
        for i in range(N,1,-1):
            self.mConfig['Recent']['{0}'.format(i)] = self.mConfig['Recent']['{0}'.format(i-1)]
        self.mConfig['Recent']['1'] = recentFile
        

    