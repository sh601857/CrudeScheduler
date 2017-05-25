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
        
        proc = subprocess.Popen(['C:\\GAMS\\win64\\24.7\\gams.exe','CrudeScheduler.gms'], stdout=subprocess.PIPE, 
                              cwd='D:\\cases\\ics\\ics2\\gms') 
        
        while proc.returncode == None: 
            msg = proc.stdout.readline()
            print(msg)
            appPro.mLogWdg.logAppend(msg,True)
        
        appPro.mLogWdg.logAppend( self.tr('Opt Finished') ,True)
        pass   