#coding=utf-8 

from PySide.QtCore import *
from PySide.QtGui import *
import subprocess  
import AppProject


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
        
        p = subprocess.Popen(['C:\\GAMS\\win64\\24.7\\gams.exe','CrudeSchMOS_CZ_RunOP.gms', 'Lo=3'], bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                              cwd='D:\\cases\\ics\\ics2\\gms') 
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
