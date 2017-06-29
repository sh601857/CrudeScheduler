#coding=utf-8 

import pandas as pd
import xlwings as xw

def run(xlFile, GamsDatFolder):

    wb = xw.Book(xlFile)
    wb.api.Application.WindowState = -4140 # xlMinimized
    set_W = []
    
    file_WRR = open(GamsDatFolder + u'Set_WRR.dat', 'w')
    sht = wb.sheets['Operations']
    for i in range(2,100):    
        w=sht.range('A{0}'.format(i)).value
        if w != None:
            #set_W.append( w )
            From = sht.range('B{0}'.format(i)).value
            if From.find(',') > 0:
                From='({0})'.format(From)
            To = sht.range('C{0}'.format(i)).value
            file_WRR.write('{0:.0f}.{1}.{2}\n'.format(w,From,To) )
        else:
            break
    file_WRR.close()
    
    file_Set_T = open( GamsDatFolder + u'Set_T.dat', 'w')
    setT = wb.sheets['Settings'].range('E2').value
    file_Set_T.write('1*{0:.0f}'.format(setT) )
    file_Set_T.close()  
    
    file_Par_H = open(GamsDatFolder + u'Par_H.dat', 'w')
    parH = wb.sheets['Settings'].range('D2').value
    file_Par_H.write('{0:.4f}'.format(parH) )
    file_Par_H.close()
    
    file_Par_minBC = open(GamsDatFolder + u'Par_minBC.dat', 'w')
    file_Par_minBC.write('{0:.0f}'.format(wb.sheets['Settings'].range('B4').value) )
    file_Par_minBC.close()
    file_Par_maxBC = open(GamsDatFolder + u'Par_maxBC.dat', 'w')
    file_Par_maxBC.write('{0:.0f}'.format(wb.sheets['Settings'].range('B5').value) )
    file_Par_maxBC.close()
    
    file_Par_RVAT = open(GamsDatFolder + u'Par_RVAT.dat', 'w')
    file_Par_RVLT = open(GamsDatFolder + u'Par_RVLT.dat', 'w')
    sht = wb.sheets['CrudeReceipts']
    for i in range(2,100):    
        rv = sht.range('A{0}'.format(i)).value
        if rv != None:
            file_Par_RVAT.write('{0} {1:.4f} \n'.format(rv, sht.range('O{0}'.format(i)).value) )
            file_Par_RVLT.write('{0} {1:.4f} \n'.format(rv, sht.range('P{0}'.format(i)).value) )
        else:
            break
    file_Par_RVAT.close()
    file_Par_RVLT.close() 
    
    file_Par_TrTime = open(GamsDatFolder + u'Par_TrTime.dat', 'w')
    file_Par_TLL = open(GamsDatFolder + u'Par_TLL.dat', 'w')
    file_Par_TLU = open(GamsDatFolder + u'Par_TLU.dat', 'w')
    file_Par_TCL0= open(GamsDatFolder + u'Par_TCL0.dat', 'w')
    sht = wb.sheets['Tanks']
    for i in range(2,100):    
        r = sht.range('A{0}'.format(i)).value
        if r != None:
            file_Par_TrTime.write('{0} {1:.4f} \n'.format(r, sht.range('L{0}'.format(i)).value / 24.0 ) )
            file_Par_TLL.write('{0} {1:.4f} \n'.format(r, sht.range('R{0}'.format(i)).value / 10000.0 ) )
            file_Par_TLU.write('{0} {1:.4f} \n'.format(r, sht.range('S{0}'.format(i)).value / 10000.0 ) )
            
            crudes = sht.range('O{0}'.format(i)).value.split(':')
            totalL = sht.range('Q{0}'.format(i)).value / 10000.0
            if len(crudes)>1:
                sfracs = sht.range('P{0}'.format(i)).value.split(':')       
                ffracs = []
                sum = 0.0
                for sf in sfracs:
                    ffracs.append( float(sf) )
                    sum = ffracs[-1] + sum
                for c in range(0,len(crudes)):
                    file_Par_TCL0.write('{0}.{1} {2:.4f} \n'.format(r, crudes[c], totalL*ffracs[c]/sum) )
            else:
                file_Par_TCL0.write('{0}.{1} {2:.4f} \n'.format(r, crudes[0], totalL) )
        else:
            break
    sht = wb.sheets['CrudeReceipts']
    for i in range(2,100):    
        rv = sht.range('A{0}'.format(i)).value
        if rv != None:
            totalL = sht.range('D{0}'.format(i)).value / 10000.0
            crudes = sht.range('B{0}'.format(i)).value.split(':')
            if len(crudes)>1:
                sfracs = sht.range('C{0}'.format(i)).value.split(':')       
                ffracs = []
                sum = 0.0
                for sf in sfracs:
                    ffracs.append( float(sf) )
                    sum = ffracs[-1] + sum
                for c in range(0,len(crudes)):
                    file_Par_TCL0.write('{0}.{1} {2:.4f} \n'.format(rv, crudes[c], totalL*ffracs[c]/sum) )
            else:
                file_Par_TCL0.write('{0}.{1} {2:.4f} \n'.format(rv, crudes[0], totalL) )   
        else:
            break
    file_Par_TrTime.close() 
    file_Par_TLL.close() 
    file_Par_TLU.close() 
    file_Par_TCL0.close() 
    
    file_Par_G= open(GamsDatFolder + u'Par_G.dat', 'w')
    file_Par_X= open(GamsDatFolder + u'Par_X.dat', 'w')
    sht = wb.sheets['Crudes']
    for i in range(2,100):    
        c = sht.range('A{0}'.format(i)).value
        if c != None:
            file_Par_G.write('{0} {1:.4f} \n'.format(c, sht.range('C{0}'.format(i)).value ) )
            file_Par_X.write('{0}.K1 {1:.4f}, {0}.K2 {2:.4f}\n'.format(c, sht.range('D{0}'.format(i)).value , sht.range('E{0}'.format(i)).value ) ) 
        else:
            break
    file_Par_G.close() 
    file_Par_X.close() 
    
    
    file_Par_CDUDL = open(GamsDatFolder + u'Par_CDUDL.dat', 'w')
    file_Par_CDUDU = open(GamsDatFolder + u'Par_CDUDU.dat', 'w')
    file_Par_XL = open(GamsDatFolder + u'Par_XL.dat', 'w')
    file_Par_XU = open(GamsDatFolder + u'Par_XU.dat', 'w')
    sht = wb.sheets['CDUs']
    #parH = wb.sheets['Settings'].range('D2').value
    for i in range(2,100):    
        u = sht.range('A{0}'.format(i)).value
        if u != None:
            file_Par_CDUDL.write('{0} {1:.4f} \n'.format(u, sht.range('J{0}'.format(i)).value / 10000.0 ) )
            file_Par_CDUDU.write('{0} {1:.4f} \n'.format(u, sht.range('K{0}'.format(i)).value / 10000.0 ) )
            file_Par_XL.write('({0}).K1 {1:.4f}, {0}.K2 {2:.4f}\n'.format(sht.range('E{0}'.format(i)).value, sht.range('F{0}'.format(i)).value , sht.range('H{0}'.format(i)).value ) ) 
            file_Par_XU.write('({0}).K1 {1:.4f}, {0}.K2 {2:.4f}\n'.format(sht.range('E{0}'.format(i)).value, sht.range('G{0}'.format(i)).value , sht.range('I{0}'.format(i)).value ) ) 
        else:
            break
    file_Par_CDUDL.close()
    file_Par_CDUDU.close()  
    file_Par_XL.close()
    file_Par_XU.close()
    
    file_Par_FRL = open(GamsDatFolder + u'Par_FRL.dat', 'w')
    file_Par_FRU = open(GamsDatFolder + u'Par_FRU.dat', 'w')
    file_Par_VL = open(GamsDatFolder + u'Par_VL.dat', 'w')
    file_Par_VU = open(GamsDatFolder + u'Par_VU.dat', 'w')
    file_Par_DURL = open(GamsDatFolder + u'Par_DURL.dat', 'w')
    sht = wb.sheets['Operations']
    for i in range(2,100):    
        w = sht.range('A{0}'.format(i)).value
        if w != None:
            file_Par_DURL.write('{0:.0f} {1:.4f}\n'.format(w, sht.range('E{0}'.format(i)).value) )
            file_Par_FRL.write('{0:.0f} {1:.4f}\n'.format(w, sht.range('F{0}'.format(i)).value) )
            file_Par_FRU.write('{0:.0f} {1:.4f}\n'.format(w, sht.range('G{0}'.format(i)).value) )
            file_Par_VL.write('{0:.0f} {1:.4f}\n'.format(w, sht.range('H{0}'.format(i)).value) )
            file_Par_VU.write('{0:.0f} {1:.4f}\n'.format(w, sht.range('I{0}'.format(i)).value) )
        else:
            break
    file_Par_FRL.close()
    file_Par_FRU.close()
    file_Par_VL.close()
    file_Par_VU.close()
    file_Par_DURL.close()
    
    
    file_Set_iCD = open(GamsDatFolder + u'Set_iCD.dat', 'w')
    file_Set_CarH = open(GamsDatFolder + u'Set_CarH.dat', 'w')
    file_Par_minN = open(GamsDatFolder + u'Par_minN.dat', 'w')
    file_Par_maxN = open(GamsDatFolder + u'Par_maxN.dat', 'w')
    sht = wb.sheets['Card']
    for i in range(2,100):    
        c = sht.range('A{0}'.format(i)).value
        if c != None:
            file_Set_iCD.write('{0}\n'.format(c) )
            file_Set_CarH.write('{0}.({1})\n'.format(c,sht.range('B{0}'.format(i)).value) )
            file_Par_minN.write('{0}  {1}\n'.format(c,sht.range('C{0}'.format(i)).value) )
            file_Par_maxN.write('{0}  {1}\n'.format(c,sht.range('D{0}'.format(i)).value) )
        else:
            break
    #file_Set_iCD.close()
    #file_Set_CarH.close()
    #file_Par_minN.close()
    #file_Par_maxN.close()
    
    file_Set_iCDT1 = open(GamsDatFolder + u'Set_iCDT1.dat', 'w')
    file_Set_CarT1 = open(GamsDatFolder + u'Set_CarT1.dat', 'w')
    file_Par_minN1 = open(GamsDatFolder + u'Par_minN1.dat', 'w')
    file_Par_maxN1 = open(GamsDatFolder + u'Par_maxN1.dat', 'w')
    sht = wb.sheets['Card']
    for i in range(2,100):    
        c = sht.range('F{0}'.format(i)).value
        if c != None:
            file_Set_iCDT1.write('{0}\n'.format(c) )
            file_Set_CarT1.write('{0}.({1})\n'.format(c,sht.range('G{0}'.format(i)).value) )
            file_Par_minN1.write('{0}  {1}\n'.format(c,sht.range('H{0}'.format(i)).value) )
            file_Par_maxN1.write('{0}  {1}\n'.format(c,sht.range('I{0}'.format(i)).value) )
        else:
            break
    file_Set_iCDT1.close()
    file_Set_CarT1.close()
    file_Par_minN1.close()
    file_Par_maxN1.close()
    
    file_Set_iCDT = open(GamsDatFolder + u'Set_iCDT.dat', 'w')
    file_Set_CarT = open(GamsDatFolder + u'Set_CarT.dat', 'w')
    file_Par_minNT = open(GamsDatFolder + u'Par_minNT.dat', 'w')
    file_Par_maxNT = open(GamsDatFolder + u'Par_maxNT.dat', 'w')
    sht = wb.sheets['Card']
    for i in range(2,100):    
        c = sht.range('K{0}'.format(i)).value
        if c != None:
            file_Set_iCDT.write('{0}\n'.format(c) )
            file_Set_CarT.write('{0}.({1})\n'.format(c,sht.range('L{0}'.format(i)).value) )
            file_Par_minNT.write('{0}  {1}\n'.format(c,sht.range('M{0}'.format(i)).value) )
            file_Par_maxNT.write('{0}  {1}\n'.format(c,sht.range('N{0}'.format(i)).value) )
        else:
            break
    file_Set_iCDT.close()
    file_Set_CarT.close()
    file_Par_minNT.close()
    file_Par_maxNT.close()
    
    file_Par_runOpTS = open(GamsDatFolder + u'Par_runOpTS.dat', 'w')
    file_Par_runOpTE = open(GamsDatFolder + u'Par_runOpTE.dat', 'w')
    file_Par_runOpV  = open(GamsDatFolder + u'Par_runOpV.dat', 'w')
    sht = wb.sheets['RuningOps']
    for i in range(2,100):    
        w = sht.range('B{0}'.format(i)).value
        if w != None:
            file_Par_runOpTS.write('{0}  {1:.4f}\n'.format(w,sht.range('O{0}'.format(i)).value) )
            file_Par_runOpTE.write('{0}  {1:.4f}\n'.format(w,sht.range('P{0}'.format(i)).value) )
            file_Par_runOpV.write('{0}  {1:.4f}\n'.format(w,sht.range('E{0}'.format(i)).value / 10000.0) )
        else:
            break
    file_Par_runOpTS.close()
    file_Par_runOpTE.close()
    file_Par_runOpV.close()

    file_Par_preOpTS = open(GamsDatFolder + u'Par_preOpTS.dat', 'w')
    file_Par_preOpTE = open(GamsDatFolder + u'Par_preOpTE.dat', 'w')
    file_Par_preOpV  = open(GamsDatFolder + u'Par_preOpV.dat', 'w') 
    file_Par_preOpTCon  = open(GamsDatFolder + u'Par_preOpTCon.dat', 'w') 
    file_Par_preOpNOM  = open(GamsDatFolder + u'Par_preOpNOM.dat', 'w') 
    file_Set_preOp  = open(GamsDatFolder + u'Set_preOp.dat', 'w') 
    
    file_WRR = open(GamsDatFolder + u'Set_WRR.dat', 'a')
    sht = wb.sheets['PreSchOps']
    for i in range(2,100):    
        w = sht.range('B{0}'.format(i)).value
        enable = sht.range('J{0}'.format(i)).value
        if w != None and enable == 1: 
            set_W.append( w )
            file_Set_preOp.write('{0}\n'.format(w) )
            file_Set_iCD.write('{0}\n'.format(w) )
            file_Set_CarH.write('{0}.{1}\n'.format(w,w) )
            file_Par_minN.write('{0}  {1}\n'.format(w,1) )
            file_Par_maxN.write('{0}  {1}\n'.format(w,1) )            
                      
            file_Par_preOpTS.write('{0}  {1:.4f}\n'.format(w,sht.range('O{0}'.format(i)).value) )
            file_Par_preOpTE.write('{0}  {1:.4f}\n'.format(w,sht.range('P{0}'.format(i)).value) )
            file_Par_preOpV.write('{0}  {1:.4f}\n'.format(w,sht.range('I{0}'.format(i)).value / 10000.0) ) 
            if sht.range('K{0}'.format(i)).value == 'Range' :
                file_Par_preOpTCon.write('{0}  {1:.0f}\n'.format(w,1) )
            elif sht.range('K{0}'.format(i)).value == 'Fixed' :
                file_Par_preOpTCon.write('{0}  {1:.0f}\n'.format(w,2) )
            preNomOps = sht.range('H{0}'.format(i)).value
            if preNomOps != None :
                file_Par_preOpNOM.write('({1}).{0}\n'.format(w, preNomOps ) )
            
            From = sht.range('C{0}'.format(i)).value
            To = sht.range('D{0}'.format(i)).value
            if From != None and To != None:
                if From.find(',') > 0:
                    From='({0})'.format(From)
                file_WRR.write('{0}.{1}.{2}\n'.format(w,From,To) ) 
                
    file_Par_preOpTS.close()
    file_Par_preOpTE.close()
    file_Par_preOpV.close() 
    file_Par_preOpTCon.close()
    file_Par_preOpNOM.close()
    file_WRR.close()
    file_Set_preOp.close()
    
    file_Set_iCD.close()
    file_Set_CarH.close()
    file_Par_minN.close()
    file_Par_maxN.close()    
    
    # wb.save()     
    # wb.close()

#run(u'D:\\cases\\ics\\ics2\\Excel\\CrudeScheduler.xlsm', u'D:\\cases\\ics\\ics2\\gms\\GamsDat\\')

