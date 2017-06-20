#coding=utf-8 

from PySide.QtCore import *
from PySide.QtGui import *
import subprocess  
import AppProject
import GenGamsDat
from pathlib import Path

class RunOptWidget(QWidget):

    def __init__(self):
        super(RunOptWidget, self).__init__()     
        self.initUI()

    def initUI(self): 
        
        self.runOptBtn = QPushButton(self.tr("Run")) 
        self.tdRunName = QLineEdit(u'Run1')
        hl1 =  QHBoxLayout()
        hl1.addWidget(self.tdRunName)
        hl1.addWidget(self.runOptBtn)
        vl1 = QVBoxLayout()
        vl1.addLayout(hl1)
        vl1.addStretch()
        self.setLayout(vl1)
        
        self.runOptBtn.clicked.connect( self.runOpt )
        
    @Slot()
    def runOpt(self):  
        appPro = AppProject.AppProject()
        appPro.mLogWdg.logAppend( self.tr('Opt Began') ,True)
        xlFile = appPro.getPath('Excel' , 'CrudeScheduler.xlsm')
        if xlFile == '' or Path( xlFile ).exists() == False:
            appPro.mLogWdg.logAppend('[CrudeScheduler.xlsm] not found',True)
            return
        GamsDatFolder = appPro.getPath('gms' , 'GamsDat') + '\\'
        if xlFile == '' :
            appPro.mLogWdg.logAppend('[GamsDat] not found',True)
            return        
        GenGamsDat.run(xlFile, GamsDatFolder)       
        appCon = AppProject.AppConfig()
        pd = subprocess.Popen([appCon.mConfig['Paths']['gams'], 'CrudeSchMOS_CZ_Data.gms', 'Lo=3'], bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                              cwd= appPro.getPath('gms' , ''))        
        pd.wait()
        
        p = subprocess.Popen([appCon.mConfig['Paths']['gams'], 'CrudeSchMOS_CZ_RunOP.gms', 'Lo=3'], bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                              cwd= appPro.getPath('gms' , ''))
        
        #p = subprocess.Popen(['dir'], shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1,
        #                              cwd='D:\\cases\\ics\\ics2\\gms') 
        for line in iter(p.stdout.readline, b''):
            print(line)
            #print (line.decode('gb2312'))  
            msgLine = line.decode('gb2312')
            msgLine = msgLine.replace('\r\n','')
            appPro.mLogWdg.logAppend(msgLine,True)
  
        p.stdout.close()
        p.wait()                
        appPro.mLogWdg.logAppend( self.tr('Opt Finished') ,True)
