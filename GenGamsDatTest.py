#coding=utf-8 

from pathlib import Path
import pandas as pd
import xlwings as xw

def run(xlFile, GamsDatFolder):

    wb = xw.Book(xlFile)
    wb.api.Application.WindowState = -4140 # xlMinimized
    set_W = []
    
    gamsdatf = Path(GamsDatFolder)
    if not gamsdatf.exists() :
        gamsdatf.mkdir()
    
    # PP sheet
    file_K = open(GamsDatFolder + u'Set_K.dat', 'w')
    file_Par_KLBP = open(GamsDatFolder + u'Set_KLBP.dat', 'w')
    file_Par_KUBP = open(GamsDatFolder + u'Set_KUBP.dat', 'w')
    
    sht = wb.sheets['PP']
    num_K=0
    for i in range(2,100):    
        k=sht.range('A{0}'.format(i)).value
        if k != None:
            file_K.write('{0}\n'.format(k) )
            file_Par_KLBP.write('{0} {1:.4f}\n'.format(k, sht.range('C{0}'.format(i)).value ) )
            file_Par_KUBP.write('{0} {1:.4f}\n'.format(k, sht.range('D{0}'.format(i)).value ) )
            num_K = num_K + 1
        else:
            break
    file_K.close()
    file_Par_KLBP.close()
    file_Par_KUBP.close()

    
    # wb.save()     
    # wb.close()

run(u'D:\\Github\\CrudeScheduler\\dat\\CrudeScheduler.xlsm', u'D:\\case\\ics\\ics2\\gms\\GamsDat\\')

