#coding=utf-8 

import tkinter.filedialog
import sys
import os
from pathlib import Path
from PySide import QtCore
from PySide import QtGui
import xlwings as xw

import AppProject
import PlotWidget
import LogWidget
import RunOptWidget



class MainW(QtGui.QMainWindow):

    def __init__(self):
        super(MainW, self).__init__()
        self.initUI()

    def initUI(self):
        
        appCon = AppProject.AppConfig()
        appCon.load()
        
        self.setWindowIcon(QtGui.QIcon('CrudeScheduler.ico'))
        if (os.name == 'nt'):
            # This is needed to display the app icon on the taskbar on Windows 7
            import ctypes
            myappid = 'iCrudeScheduler.1.0.0' # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)          
        
        
        self._createCMDDock() #Create cmd tree dockwidget
        
        self._createLogDock() #Create log dockwidget

        self._createCentralWgt() #Create central widget	
        
        self._createActionMenuToolBar() #Create actions menu and toolbar	
        
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('iCrudeScheduler')    
        self.showMaximized()

        # Connests signals and slots
        self.cmdTree.clicked.connect(self.setWidget)
        self.cmdTree.doubleClicked.connect(self.cmdDoubleClicked)
        
        # Reset left dock width  after app starts
        QtCore.QTimer.singleShot(200, self.resetDockWidth)
        
    @QtCore.Slot()
    def resetDockWidth(self):
        self.cmdTree.setMinimumWidth(10)

    def setCensWgt(self,wgtID):
        if wgtID == 1001:
            #self.censw.setCurrentWidget(self.simSpecWgt)
            #self.simSpecWgt.loadData()   
            pass
        elif wgtID == 2001:
            self.censw.setCurrentWidget(self.runOptWidget)
        elif 2002 == wgtID:
            self.censw.setCurrentWidget(self.plotWidget)
            self.plotWidget.loadData()
        else:
            self.censw.setCurrentWidget(self.emptyPageWidget)
            
        self._curWgtID = wgtID
        
    @QtCore.Slot()
    def setWidget(self,index):
        wgtID = self.cmdmodel.itemFromIndex(index).data(QtCore.Qt.UserRole+1)
        if( self._curWgtID != wgtID):        
            self.setCensWgt(wgtID)
            
    @QtCore.Slot()
    def cmdDoubleClicked(self,index):
        wgtID = self.cmdmodel.itemFromIndex(index).data(QtCore.Qt.UserRole+1)
        activeSheetName = ''
        if wgtID == 1001: 
            activeSheetName = 'Crudes'
        elif wgtID == 1002:
            activeSheetName = 'Tanks'
        elif wgtID == 1003:
            activeSheetName = 'Pipelines'  
        elif wgtID == 1004:
            activeSheetName = 'CDUs' 
        elif wgtID == 1005:
            activeSheetName = 'Operations' 
        elif wgtID == 2001:
            if( self._curWgtID != wgtID):        
                self.setCensWgt(wgtID)  
                
        if activeSheetName != '':
            appPro = AppProject.AppProject()
            xlFile = appPro.getPath('Excel' , 'CrudeScheduler.xlsm')
            if xlFile == '' or Path( xlFile ).exists() == False:
                appPro.mLogWdg.logAppend('[CrudeScheduler.xlsm] not found',True)
                return            
            wb = xw.Book(xlFile) 
            ws = wb.sheets[activeSheetName]
            ws.activate()
            wb.activate(steal_focus=True)
            wb.api.Application.WindowState = -4143
                   

    @QtCore.Slot()
    def newProject(self):            
        fileName = QtGui.QFileDialog.getSaveFileName(self, self.tr("New project"), "", self.tr("iCrudeScheduler Project Files (*.icsp)")  ) [0]
        if fileName == '':
            return 
        print( fileName )
        
        appPro = AppProject.AppProject()
        appPro.mFilePath = fileName
        appPro.save()
        appPro.creatFolder()
        self.setCensWgt(0)
        
        self.setWindowTitle( 'iCrudeScheduler[{0}]'.format( appPro.mFilePath ) )
        appPro.mLogWdg.clearLog()
        appPro.mLogWdg.logAppend( self.tr('Project [{0}] cteated.').format( appPro.mFilePath ) ,True)
        appCon = AppProject.AppConfig()
        appCon.pushRecent(appPro.mFilePath)        
        
    @QtCore.Slot()
    def openProject(self):
        appCon = AppProject.AppConfig()
        opDir = appCon.mConfig['Recent']['1']
        if opDir!= u'':
            opDir = str( Path(opDir).parent )
        
        fileName = QtGui.QFileDialog.getOpenFileName( self, self.tr("Open project"), opDir, self.tr("iCrudeScheduler Project Files (*.icsp)") ) [0]
        if fileName == '':
            return 
        print( fileName )
        appPro = AppProject.AppProject()
        appPro.mFilePath = fileName
        appPro.load()
        
        self.setWindowTitle( 'iCrudeScheduler[{0}]'.format( appPro.mFilePath ) )
        self.setCensWgt(0)
        appPro.mLogWdg.clearLog()
        appPro.mLogWdg.logAppend( self.tr('Project [{0}] opend.').format( appPro.mFilePath ) ,True)
        appCon.pushRecent(appPro.mFilePath)
        
    @QtCore.Slot()
    def closeProject(self):            

        pass
    
    @QtCore.Slot()
    def save(self):            
        appPro = AppProject.AppProject()
        # save current working widget
        
        # save project file
        if appPro.mFilePath != u'':
            appPro.save()
            
            
    def _createCMDDock(self):  

        def createItem( itemData ):
            item = QtGui.QStandardItem( itemData['text'] )
            item.setData(itemData['ID'], QtCore.Qt.UserRole+1)
            item.setFlags( itemData['Flags'] )
            return item
        # create commonds tree  
        self.cmdmodel = QtGui.QStandardItemModel()
        parentItem = self.cmdmodel.invisibleRootItem()            
        item = createItem({'text':'1.Specification','ID':1001,'Flags': QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled, })
        item.appendRow( createItem({'text':'Crudes','ID':1001,'Flags': QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled, }) )
        item.appendRow( createItem({'text':'Tanks', 'ID':1002,'Flags': QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled, }) )
        item.appendRow( createItem({'text':'Pipelines', 'ID':1003,'Flags': QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled, }) )
        item.appendRow( createItem({'text':'CDUS', 'ID':1004,'Flags': QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled, }) )
        item.appendRow( createItem({'text':'Operations', 'ID':1005,'Flags': QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled, }) )
        parentItem.appendRow(item)
        
        item = createItem({'text':'2.Optimization','ID':2001,'Flags': QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled, })
        item.appendRow( createItem({'text':'Shecdule','ID':2002,'Flags': QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled, }) )
        parentItem.appendRow(item)
  
        self.cmdTree = QtGui.QTreeView(self)
        self.cmdTree.setModel(self.cmdmodel)
        self.cmdTree.setHeaderHidden(True)
        self.cmdTree.expandToDepth(2)
        self.cmdTree.setMinimumWidth(150)
    
        dockWidget = QtGui.QDockWidget((""), self)
        dockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        dockWidget.setWidget(self.cmdTree)
        dockWidget.setBaseSize(200,800)
        dockWidget.setTitleBarWidget(QtGui.QWidget(dockWidget))
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dockWidget)#hide the titlebar        
  
    def _createLogDock(self):
        self.logWgt = LogWidget.LogWidget()
        appPro = AppProject.AppProject()
        appPro.mLogWdg = self.logWgt   # AppProject hold LogWidget for clients 
    
        self._dockLogWgt = QtGui.QDockWidget(self.tr("Log"), self)
        self._dockLogWgt.setWidget( self.logWgt )
        self._dockLogWgt.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        self._dockLogWgt.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self._dockLogWgt.setFeatures( QtGui.QDockWidget.DockWidgetClosable | QtGui.QDockWidget.DockWidgetMovable | QtGui.QDockWidget.DockWidgetFloatable)
        self._dockLogWgt.setMinimumHeight(  60 )
        self._dockLogWgt.setMaximumHeight( 600 )
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self._dockLogWgt)
        self.setCorner( QtCore.Qt.BottomLeftCorner, QtCore.Qt.LeftDockWidgetArea )
        
    def _createCentralWgt(self) :

        self.emptyPageWidget =  QtGui.QWidget()
        self.plotWidget = PlotWidget.PlotWidget()
        self.runOptWidget = RunOptWidget.RunOptWidget()
    
        self.censw =  QtGui.QStackedWidget()
        self.censw.addWidget(self.emptyPageWidget)
        self.censw.addWidget(self.runOptWidget)
        self.censw.addWidget(self.plotWidget)
    
        self.censw.setCurrentIndex(0)
        self._curWgtID = 0
    
        self.setCentralWidget(self.censw)   
        
        
    def _createActionMenuToolBar(self):
        # Actions
        newProAct = QtGui.QAction(self.tr('New Project'), self)
        #newProAct.setShortcut('Ctrl+Q')
        newProAct.setStatusTip(self.tr('Create a new porject'))
        newProAct.triggered.connect(self.newProject)        
    
        openProAct = QtGui.QAction(self.tr('Open Project'), self)
        #openProAct.setShortcut('Ctrl+Q')
        openProAct.setStatusTip(self.tr('Open a existing porject'))
        openProAct.triggered.connect(self.openProject)  
    
        closeProAct = QtGui.QAction(self.tr('Close project'), self)
        #closeProAct.setShortcut('Ctrl+Q')
        closeProAct.setStatusTip(self.tr('Close project'))
        closeProAct.triggered.connect(self.closeProject) 
    
        saveAct = QtGui.QAction(self.tr('Save'), self)
        #saveAct.setShortcut('Ctrl+Q')
        saveAct.setStatusTip(self.tr('Save'))
        saveAct.triggered.connect(self.save)  
    
        exitAction = QtGui.QAction(self.tr('Exit'), self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip(self.tr('Exit application') )
        exitAction.triggered.connect(self.close)
    
        self.statusBar()
        # menus
        menubar = self.menuBar()
        fileMenu = menubar.addMenu(self.tr('&File'))
        fileMenu.addAction(newProAct)
        fileMenu.addAction(openProAct)
        fileMenu.addAction(closeProAct)
        fileMenu.addAction(saveAct)
        fileMenu.addAction(exitAction)
    
        viewMenu = menubar.addMenu(self.tr('&View'))
        viewMenu.addAction( self._dockLogWgt.toggleViewAction() )
    
        toolbar = self.addToolBar(self.tr('Exit'))
        toolbar.addAction(exitAction)     
        
    def closeEvent(self, event):
        if True:
            appCon = AppProject.AppConfig()
            appCon.save()            
            event.accept()
        else:
            event.ignore()        
def main():

    app = QtGui.QApplication(sys.argv)
    ex = MainW()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
