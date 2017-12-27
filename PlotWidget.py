#coding=utf-8 

import sys
import matplotlib
matplotlib.use('Qt4Agg')
import pylab
import math
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.widgets import Slider, Button, RadioButtons,SpanSelector

from PySide.QtCore import *
from PySide.QtGui import *
from pathlib import Path
import AppProject

class ScheduleCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=9, height=6, dpi=None):
        self.fig = Figure(figsize=(width, height), facecolor=(.94,.94,.94), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)    
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)  
        self.axes = self.fig.add_axes([0.05, 0.05, 0.9, 0.9], axis_bgcolor=(.94,.94,.94))
        self.compute_initial_figure()

        # contextMenu
        acExportPlot = QAction(self.tr("Export plot"), self)
        FigureCanvas.connect(acExportPlot,SIGNAL('triggered()'), self, SLOT('exportPlot()') )
        FigureCanvas.addAction(self, acExportPlot )
        FigureCanvas.setContextMenuPolicy(self, Qt.ActionsContextMenu )

    def compute_initial_figure(self):
        self.axes.clear()
        appPro = AppProject.AppProject()
        schFile=appPro.getPath('Sol', u'MOS_CZ_schedule.csv')
        #schFile = u'D:\\cases\\ics\\ics2\\gms\\CS_MOS_CZ_schedule.csv'
        if schFile == '' or Path( schFile ).exists() == False :   # No file
            return 
        xlFile = appPro.getPath('Excel' , 'CrudeScheduler.xlsm')
        if xlFile == '' or Path( xlFile ).exists() == False:
            return 
        import xlwings as xw
        from datetime import timedelta, datetime
        wb = xw.Book(xlFile)
        wb.api.Application.WindowState = -4140 # xlMinimized  
        startDate = wb.sheets['Settings'].range('B2').value
        
        sht = wb.sheets['Plots']
        cdus =[]
        tanks=[]
        for i in range(2,100):    
            rv = sht.range('A{0}'.format(i)).value
            if rv != None:
                eutype = sht.range('B{0}'.format(i)).value
                if  eutype == u'CDU':
                    cdus.append( ( rv, sht.range('C{0}'.format(i)).value ) )
                elif eutype == u'Tank':
                    tanks.append( ( rv, sht.range('C{0}'.format(i)).value ) )
            else:
                break
                
        
        df = pd.read_csv(schFile, names=['From','To','n','TS','TE','Vol'])
        df.sort_values(by=['To','TS','From'], inplace=True)
        for i in range(1,len(df)):
            if df.iloc[i,0] == df.iloc[i-1,0] and df.iloc[i,1] == df.iloc[i-1,1] and df.iloc[i,3] == df.iloc[i-1,4]:
                df.iloc[i,3] = df.iloc[i-1,3]
                df.iloc[i,5] = df.iloc[i-1,5] + df.iloc[i,5]
                df.iloc[i-1,5] = -1;
        df = df[df.Vol>0]

        #cdus = [('CDU1',1)]
        linewidth=2
        colors=['chocolate','grey']
        colorTankIn = 'c'
        colorTankOut = 'b'
        ytk  =[]
        ytkl =[]
        for u in cdus :
            ytk.append(u[1])
            ytkl.append(u[0])
            df_u = df[df.To==u[0]]
            #print(df_u)
            for i in range(0,len(df_u)):
                #plt.plot([ df_u.iloc[i,3], df_u.iloc[i,4] ] , [u[1],u[1]],  color=colors[i%2], linewidth=linewidth)
                self.axes.bar(df_u.iloc[i,3], 0.2, width=df_u.iloc[i,4]-df_u.iloc[i,3], bottom=u[1]-0.1, color=colors[i%2], linewidth=0)
                self.axes.text(df_u.iloc[i,3], u[1]-0.4, df_u.iloc[i,0],color=colors[i%2],)

        #tanks = [('G109',2),('G102',3),('G101',4),('G184',5),('G183',6),('G182',7),('G181',8),('V2',9),('V1',10)]   
        for u in tanks :
            ytk.append(u[1])
            ytkl.append(u[0])    
            df_u = df[df.To==u[0]]  #tank in
            #print(df_u)
            for i in range(0,len(df_u)):
                #plt.plot([ df_u.iloc[i,3], df_u.iloc[i,4] ] , [u[1]+0.1,u[1]+0.1],  color=colorTankIn, linewidth=linewidth)
                self.axes.bar(df_u.iloc[i,3], 0.2, width=df_u.iloc[i,4]-df_u.iloc[i,3], bottom=u[1]+0.00, color=colorTankIn, linewidth=0)
                self.axes.text(df_u.iloc[i,3], u[1]+0.25, df_u.iloc[i,0],  color=colorTankIn)

        for u in tanks :
            df_u = df[df.From==u[0]] #tank Out
            #print(df_u)
            for i in range(0,len(df_u)):
                #plt.plot([ df_u.iloc[i,3], df_u.iloc[i,4] ] , [u[1]-0.1,u[1]-0.1],  color=colorTankOut, linewidth=linewidth)
                self.axes.bar(df_u.iloc[i,3], 0.2, width=df_u.iloc[i,4]-df_u.iloc[i,3], bottom=u[1]-0.20, color=colorTankOut, linewidth=0)
                self.axes.text(df_u.iloc[i,3], u[1]-0.45, df_u.iloc[i,1],color=colorTankOut)

        self.axes.set_ylim( 0, 11 ) 
        self.axes.set_yticks(ytk)
        self.axes.set_yticklabels(ytkl)        
        self.axes.set_xlim(df['TS'].min(), df['TE'].max())
        xtk = range(0, math.ceil(df['TE'].max() +1), 1 )
        xtkl = [(startDate+timedelta(days=x)).strftime("%y/%m/%d %H:%M") for x in xtk]
        #print(xtkl)
        self.axes.set_xticks( xtk )
        self.axes.set_xticklabels( xtkl )

        self.axes.set_title( u'**石化2017年*月原油运输调度方案' )
        #self.axes.set_xlabel(u'天')
        self.draw_idle()

    def exportPlot(self):

        fileName = QFileDialog.getSaveFileName( self, self.tr("Save figure"), "", ("PNG file (*.png)") ) [0]
        if fileName == '':   # No file selected
            return  
        self.fig.savefig( fileName, format='png' )


class TankInvCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=9, height=12, dpi=None, invRange='E1:H7'):
        
        self.fig = Figure(figsize=(width, height), facecolor=(.94,.94,.94), dpi=dpi)
        
        #self.axes = self.fig.subplots(nrows=2, ncols=3, sharex=True)
        #self.fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.05, hspace=0.05)  
        self.axes=[]
        
        
        self.axes.append( self.fig.add_axes([0.05, 0.55, 0.28, 0.4]) )
        self.axes.append( self.fig.add_axes([0.36, 0.55, 0.28, 0.4]) )
        self.axes.append( self.fig.add_axes([0.67, 0.55, 0.28, 0.4]) )
        self.axes.append( self.fig.add_axes([0.05, 0.05, 0.28, 0.4]) )
        self.axes.append( self.fig.add_axes([0.36, 0.05, 0.28, 0.4]) )
        self.axes.append( self.fig.add_axes([0.67, 0.05, 0.28, 0.4]) )

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)    
        FigureCanvas.setSizePolicy(self,QSizePolicy.Expanding,QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)  
        self.tkscell=invRange
        #self.compute_initial_figure()

        # contextMenu
        acExportPlot = QAction(self.tr("Export plot"), self)
        FigureCanvas.connect(acExportPlot,SIGNAL('triggered()'), self, SLOT('exportPlot()') )
        FigureCanvas.addAction(self, acExportPlot )
        FigureCanvas.setContextMenuPolicy(self, Qt.ActionsContextMenu )

    def compute_initial_figure(self):
        for ax in self.axes:
            ax.clear()

        appPro = AppProject.AppProject()
        invFile=appPro.getPath('Sol', u'MOS_CZ_TankInv.csv')
        if invFile == '' or Path( invFile ).exists() == False :   # No file
            return 
        xlFile = appPro.getPath('Excel' , 'CrudeScheduler.xlsm')
        if xlFile == '' or Path( xlFile ).exists() == False:
            return 
        import xlwings as xw
        from datetime import timedelta, datetime
        wb = xw.Book(xlFile)
        wb.api.Application.WindowState = -4140 # xlMinimized  
        startDate = wb.sheets['Settings'].range('B2').value
        sht = wb.sheets['Plots']
        
        pdInv = sht.range(self.tkscell).options(pd.DataFrame).value
        pdInv.dropna(inplace=True)
        if len(pdInv) < 1:
            return
        tanks = pdInv['Tank'].values       
        #tanks = ['G181','G182','G101','G183','G184','G102']
        df = pd.read_csv(invFile, names=['Tank','n','TE','Vol'])

        for i in range(0,len(tanks)):
            df_u = df[df.Tank==tanks[i]]
            ax = self.axes[i]
            ax.set_axis_bgcolor((.94,.94,.94))
            ax.plot(df_u.TE, df_u.Vol)
            ax.set_title(tanks[i])
            ax.set_ylim( pdInv.loc[i,'ylowb'], pdInv.loc[i,'yupb'] )
            
            #if i%3 == 2:
                #ax.set_ylim( 0, 1.5 )
            #else:
                #ax.set_ylim( 0, 5.0 ) 
            
        xtk = range(0, math.ceil(df['TE'].max() +1), 1 )
        #xtkl = [(startDate+timedelta(days=x)).strftime("%y/%m/%d %H:%M") for x in xtk]
        xtkl = ['' for x in xtk]
        xtkl[0] = (startDate+timedelta(days=xtk[0])).strftime("%y/%m/%d %H:%M")
        xtkl[-1] = (startDate+timedelta(days=xtk[-1])).strftime("%y/%m/%d %H:%M")
        self.axes[0].set_xlim(df['TE'].min(), df['TE'].max())
        self.axes[0].set_xticks( xtk )
        self.axes[0].set_xticklabels( xtkl, alpha=0.0 ) 
        self.axes[1].set_xticklabels( xtkl, alpha=0.0 )
        self.axes[2].set_xticklabels( xtkl, alpha=0.0 )
        self.axes[3].set_xticklabels( xtkl )
        self.axes[4].set_xticklabels( xtkl , alpha=0.0 )
        self.axes[5].set_xticklabels( xtkl , alpha=0.0 )

        self.draw_idle()

    def exportPlot(self):  
        fileName = QFileDialog.getSaveFileName( self, self.tr("Save figure"), "", ("PNG file (*.png)") ) [0]
        if fileName == '':   # No file selected
            return  
        self.fig.savefig( fileName, format='png' )         

class CDUCKCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=9, height=12, dpi=None):
        
        self.fig = Figure(figsize=(width, height), facecolor=(.94,.94,.94), dpi=dpi)
        self.axes=[]
        
        
        self.axes.append( self.fig.add_axes([0.15, 0.55, 0.83, 0.4] ) )
        self.axes.append( self.fig.add_axes([0.15, 0.05, 0.83, 0.4] ,sharex=self.axes[0]) )
        self.axes[0].set_axis_bgcolor((.94,.94,.94))
        self.axes[1].set_axis_bgcolor((.94,.94,.94))


        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)    
        FigureCanvas.setSizePolicy(self,QSizePolicy.Expanding,QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)  

        #self.compute_initial_figure()

        # contextMenu
        acExportPlot = QAction(self.tr("Export plot"), self)
        FigureCanvas.connect(acExportPlot,SIGNAL('triggered()'), self, SLOT('exportPlot()') )
        FigureCanvas.addAction(self, acExportPlot )
        FigureCanvas.setContextMenuPolicy(self, Qt.ActionsContextMenu )
        
        
    def ax1CDURadio(self, label):
        self.axPlot(self.axes[0], label, self.activeK1)
        self.activeCDU1 = label
        self.draw_idle() 
        
    def ax2CDURadio(self, label):
        self.axPlot(self.axes[1], label, self.activeK2)
        self.activeCDU2 = label
        self.draw_idle()
        
    def ax1KRadio(self, label):
        self.axPlot(self.axes[0], self.activeCDU1, label)
        self.activeK1=label
        self.draw_idle()
        
    def ax2KRadio(self, label):
        self.axPlot(self.axes[1], self.activeCDU2, label)
        self.activeK2=label
        self.draw_idle()
        
    def axPlot(self, ax, cdu1, k1):       
        for i, line in enumerate(ax.lines):
            #ax.lines.pop(i)
            line.remove()
        dfc1 = self.df[self.df.CDU==cdu1]
        dfc1 = dfc1[dfc1.K == k1]
        if len(dfc1) < 2:
            return
        cX=[]
        cY=[]        
        for i in range( len(dfc1)):
            cX.append( dfc1.iloc[i,3] )
            cX.append( dfc1.iloc[i,4] )
            cY.append( dfc1.iloc[i,5] )
            cY.append( dfc1.iloc[i,5] )
        ax.plot( cX, cY , label=k1, linewidth=2.0, color='b')
        ax.set_title( "{0}_{1}".format(cdu1,k1)  )
        ax.set_ylim( self.pdCDUCK.loc[(cdu1,k1),'ylowb'] , self.pdCDUCK.loc[(cdu1,k1),'yupb'] )

    def compute_initial_figure(self):
        for ax in self.axes:
            ax.clear()

        appPro = AppProject.AppProject()
        invFile=appPro.getPath('Sol', u'CDUFeedCK.csv')
        if invFile == '' or Path( invFile ).exists() == False :   # No file
            return 
        xlFile = appPro.getPath('Excel' , 'CrudeScheduler.xlsm')
        if xlFile == '' or Path( xlFile ).exists() == False:
            return 
        import xlwings as xw
        from datetime import timedelta, datetime
        wb = xw.Book(xlFile)
        wb.api.Application.WindowState = -4140 # xlMinimized  
        startDate = wb.sheets['Settings'].range('B2').value
        sht = wb.sheets['Plots']
         
        self.pdCDUCK = sht.range('J1:M20').options(pd.DataFrame, index=2).value
        self.pdCDUCK.dropna(inplace=True)
        if len(self.pdCDUCK) < 1:
            return
        self.CDUs = self.pdCDUCK.index.get_level_values(0).values
        self.Ks = self.pdCDUCK.index.get_level_values(1).values
        self.CDUs = list(set(self.CDUs)) 
        self.Ks = list(set(self.Ks)) 
        
        if len(self.CDUs) >1:
            rax1 = self.fig.add_axes([0.01, 0.80, 0.15, 0.20], frameon=False)
            rax1.set_axis_bgcolor((.94,.94,.94))
            self.radioCDU1 = RadioButtons(rax1, self.CDUs)  
            #self.radioCDU1.set_active(0)
            self.radioCDU1.on_clicked(self.ax1CDURadio)        
            
            rax2 = self.fig.add_axes([0.01, 0.30, 0.15, 0.20], frameon=False)
            rax2.set_axis_bgcolor((.94,.94,.94))
            self.radioCDU2 = RadioButtons(rax2, self.CDUs) 
            #self.radioCDU2.set_active(1)
            self.radioCDU2.on_clicked(self.ax2CDURadio) 
        
        if len(self.Ks) >1:
            rax1 = self.fig.add_axes([0.01, 0.50, 0.15, 0.30], frameon=False)
            rax1.set_axis_bgcolor((.94,.94,.94))
            self.radioK1 = RadioButtons(rax1, self.Ks)  
            #self.radioK1.set_active(0)
            self.radioK1.on_clicked(self.ax1KRadio)        
            
            rax2 = self.fig.add_axes([0.01, 0.00, 0.15, 0.30], frameon=False)
            rax2.set_axis_bgcolor((.94,.94,.94))
            self.radioK2 = RadioButtons(rax2, self.Ks) 
            #self.radioK2.set_active(1)
            self.radioK2.on_clicked(self.ax2KRadio) 
        
        
        
        
        self.df = pd.read_csv(invFile, names=['CDU','K','I','TS','TE','V'])
        if len(self.df) < 2:
            return        
        
        self.axPlot(self.axes[0], self.CDUs[0], self.Ks[0] )
        self.activeCDU1 = self.CDUs[0]
        self.activeK1 = self.Ks[0]
        
        if len(self.CDUs) >1:
            self.axPlot(self.axes[1], self.CDUs[1], self.Ks[0])
            self.activeCDU2 = self.CDUs[1]
            self.activeK2 = self.Ks[0]            
        else:
            if len(self.Ks) >1:
                self.axPlot(self.axes[1], self.CDUs[0], self.Ks[1])
                self.activeCDU2 = self.CDUs[0]
                self.activeK2 = self.Ks[1]                   
                
        xtk = range(0, math.ceil(self.df['TE'].max() +1), 1 )
        xtkl = [(startDate+timedelta(days=x)).strftime("%m/%d %H:%M") for x in xtk]
        self.axes[0].set_xlim(self.df['TS'].min(), self.df['TE'].max())
        self.axes[0].set_xticks( xtk )        
        self.axes[0].set_xticklabels( xtkl, alpha=0.0 ) 
        self.axes[1].set_xticklabels( xtkl)         
        
        self.draw_idle()

    def exportPlot(self):  
        fileName = QFileDialog.getSaveFileName( self, self.tr("Save figure"), "", ("PNG file (*.png)") ) [0]
        if fileName == '':   # No file selected
            return  
        self.fig.savefig( fileName, format='png' )   




class PlotWidget(QWidget):
    def __init__(self, canvas):
        super(PlotWidget, self).__init__()
        self.canvas = canvas #
        self.initUI()

    def initUI(self):
        layout =  QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.setContentsMargins(1,1,1,1)

        self.setLayout(layout) 

    def loadData(self):
        if self.canvas!=None:
            self.canvas.compute_initial_figure()
