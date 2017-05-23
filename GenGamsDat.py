#coding=utf-8 

import pandas as pd
import xlwings as xw

wb = xw.Book(r'D:\Workspace\Crude\CrudeScheduler\CrudeScheduler.xlsm')
sht = wb.sheets['Operations']

file_WRR = open(r'D:\Workspace\Crude\CrudeScheduler\GamsDat\Set_WRR.dat', 'w')
for i in range(2,100):    
    w=sht.range('A{0}'.format(i)).value
    if w != None:
        From = sht.range('B{0}'.format(i)).value
        if From.find(',') > 0:
            From='({0})'.format(From)
        To = sht.range('C{0}'.format(i)).value
        file_WRR.write('{0:.0f}.{1}.{2}\n'.format(w,From,To) )
                
    else:
        break
file_WRR.close()   
#wb.save()     
#wb.close()