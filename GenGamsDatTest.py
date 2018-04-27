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
    file_Par_KLBP = open(GamsDatFolder + u'Par_KLBP.dat', 'w')
    file_Par_KUBP = open(GamsDatFolder + u'Par_KUBP.dat', 'w')
    
    sht = wb.sheets['PP']
    num_K=0
    list_K=[]
    for i in range(2,100):    
        k=sht.range('A{0}'.format(i)).value
        if k != None:
            file_K.write('{0}\n'.format(k) )
            file_Par_KLBP.write('{0} {1:.4f}\n'.format(k, sht.range('C{0}'.format(i)).value ) )
            file_Par_KUBP.write('{0} {1:.4f}\n'.format(k, sht.range('D{0}'.format(i)).value ) )
            num_K = num_K + 1
            list_K.append(k)
        else:
            break
    file_K.close()
    file_Par_KLBP.close()
    file_Par_KUBP.close()
    
    # CBlends
    file_CB = open(GamsDatFolder + u'Set_CB.dat', 'w')
    file_CBCDU = open(GamsDatFolder + u'Set_CBCDU.dat', 'w')
    file_Par_CBDL= open(GamsDatFolder + u'Set_CBDL.dat', 'w')
    file_Par_CBDU= open(GamsDatFolder + u'Set_CBDU.dat', 'w')
    file_Par_CBFRL= open(GamsDatFolder + u'Par_CBFRL.dat', 'w')
    file_Par_CBFRU= open(GamsDatFolder + u'Par_CBFRU.dat', 'w')
    file_Par_CBKLB = open(GamsDatFolder + u'Par_CBKLB.dat', 'w')
    file_Par_CBKUB = open(GamsDatFolder + u'Par_CBKUB.dat', 'w')    
    
    sht = wb.sheets['CBlends']
    for i in range(3,100):    
        cb=sht.range('A{0}'.format(i)).value
        if cb != None:  
            print(cb)
            file_CB.write('{0}\n'.format(cb) )
            file_CBCDU.write('{0}.{1}\n'.format(cb, sht.range('B{0}'.format(i)).value) )
            file_Par_CBDL.write('{0}  {1:.4f}\n'.format(cb, sht.range('D{0}'.format(i)).value / 10000.0 ) )
            file_Par_CBDU.write('{0}  {1:.4f}\n'.format(cb, sht.range('E{0}'.format(i)).value / 10000.0 ) )
            file_Par_CBFRL.write('{0}  {1:.4f}\n'.format(cb, sht.range('F{0}'.format(i)).value / 10000.0 ) )
            file_Par_CBFRU.write('{0}  {1:.4f}\n'.format(cb, sht.range('G{0}'.format(i)).value / 10000.0 ) )
            for k in range(0,num_K):
                file_Par_CBKLB.write('{0}.{1}  {2:.4f}\n'.format(cb, list_K[k], sht.range((i, 8+2*k  )).value) )
                file_Par_CBKUB.write('{0}.{1}  {2:.4f}\n'.format(cb, list_K[k], sht.range((i, 8+2*k+1)).value) )
        else:
            break
    
    file_CB.close()
    file_CBCDU.close()
    file_Par_CBDL.close()
    file_Par_CBDU.close()
    file_Par_CBFRL.close()
    file_Par_CBFRU.close()
    file_Par_CBKLB.close()
    file_Par_CBKUB.close()    
    
    # wb.save()     
    # wb.close()

run(u'D:\\Github\\CrudeScheduler\\dat\\CrudeScheduler.xlsm', u'D:\\case\\ics\\ics2\\gms\\GamsDat\\')

