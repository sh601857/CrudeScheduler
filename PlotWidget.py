#coding=utf-8 

import sys
import matplotlib
matplotlib.use('Qt4Agg')
import pylab

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

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=9, height=6, dpi=None):
        self.fig = Figure(figsize=(width, height), facecolor=(.94,.94,.94), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)    
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)  
        self.axes = self.fig.add_axes([0.05, 0.1, 0.9, 0.85], axis_bgcolor=(.94,.94,.94))
        self.compute_initial_figure()

        # contextMenu
        acExportPlot = QAction(self.tr("Export plot"), self)
        FigureCanvas.connect(acExportPlot,SIGNAL('triggered()'), self, SLOT('exportPlot()') )
        FigureCanvas.addAction(self, acExportPlot )
        FigureCanvas.setContextMenuPolicy(self, Qt.ActionsContextMenu )

    def compute_initial_figure(self):
        appPro = AppProject.AppProject()
        schFile=appPro.getPath('Sol', u'CS_MOS_CZ_schedule.csv')
        #schFile = u'D:\\cases\\ics\\ics2\\gms\\CS_MOS_CZ_schedule.csv'
        if schFile == '' or Path( schFile ).exists() == False :   # No file
            return 
        
        df = pd.read_csv(schFile, names=['From','To','n','TS','TE','Vol'])
        df.sort_values(by=['To','TS','From'], inplace=True)
        for i in range(1,len(df)):
            if df.iloc[i,0] == df.iloc[i-1,0] and df.iloc[i,1] == df.iloc[i-1,1] and df.iloc[i,3] == df.iloc[i-1,4]:
                df.iloc[i,3] = df.iloc[i-1,3]
                df.iloc[i,5] = df.iloc[i-1,5] + df.iloc[i,5]
                df.iloc[i-1,5] = -1;
        df = df[df.Vol>0]
        
        cdus = [('CDU1',1)]
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
        
        tanks = [('G109',2),('G102',3),('G101',4),('G184',5),('G183',6),('G182',7),('G181',8),('V2',9),('V1',10)]   
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
        self.axes.set_xlim(0, df['TE'].max())
        self.axes.set_yticks(ytk)
        self.axes.set_yticklabels(ytkl)
        self.axes.set_title( u'**石化2017年*月原油运输调度方案' )
        self.axes.set_xlabel(u'天')
        self.draw_idle()

    def exportPlot(self):

        fileName = QFileDialog.getSaveFileName( self, self.tr("Save figure"), "", ("PNG file (*.png)") ) [0]
        if fileName == '':   # No file selected
            return  
        self.fig.savefig( fileName, format='png' )

class PlotWidget(QWidget):
    def __init__(self):
        super(PlotWidget, self).__init__()     
        self.initUI()

    def initUI(self):

        self.canvas = MyMplCanvas(self, width=5, height=4)
        layout =  QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.setContentsMargins(1,1,1,1)

        self.setLayout(layout) 
    
    def loadData(self):
        self.canvas.axes.clear()
        self.canvas.compute_initial_figure()
