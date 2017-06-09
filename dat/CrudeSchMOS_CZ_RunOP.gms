$onempty
Option Limrow=0;
Option Limcol=0;
Option Solprint=off;

SETS
    I     /0
$include GamsDat/Set_T.dat
E
/
    T(I)     /
$include GamsDat/Set_T.dat
/
    N(I)     /
$include GamsDat/Set_T.dat
E
/
    C     /A,B,C,D,E,F/
    K     /K1,K2/
    W     /1*17/
    WU(W) /15*17/
    WT(W) /4*14/
    WD(W) /1*3/
    R     /V1,V2,V3, G181*G184, G101*G102,G109,TL,BL,CDU1/
    TK(R)    tanks         /G181*G184,G101*G102,G109/
    RV(R)    vessels       /V1,V2,V3/
    RS(TK)   storage tank  /G181*G184/
    RC(TK)   charging tank /G101*G102,G109/
    RD(R)    CDU           /CDU1 /
    RL(R)    Pipeline      /TL,BL  /
    FCR(R)   fixed crude   /V1,V2,V3/
    INr(R,W)
    OUr(R,W)
;
ALIAS(W,W1,W2);
ALIAS(R,R1,R2);
ALIAS(T,T1,T2);  ALIAS(I,I1,I2);  ALIAS(N,N1,N2);
ALIAS(RV,RV1,RV2);

SETS
    WRR(W,R1,R2) Operations and Units   / 1.G101.CDU1, 2.G102.CDU1, 3.G109.CDU1, 4.BL.G101, 5.BL.G102, 6.BL.G109,
    7.G181.BL, 8.G182.BL, 9.G183.BL, 10.G184.BL, 11.TL.G181, 12.TL.G182, 13.TL.G183, 14.TL.G184,
    15.V1.TL, 16.V2.TL, 17.V3.TL /
    NOM(W1,W2)   non-overlapping matrix /1.2, 1.3, 2.3, 1.4, 2.5, 3.6, 7.11, 8.12, 9.13, 10.14, 15.16, 15.17, 16.17/
    iCW  CLIQUE / 1*9 /
    CWW(iCW,W)   /
1.(1 ,2 ,3)
2.(1 ,4)
3.(5 ,2)
4.(6 ,3)
5.(7 ,11)
6.(8 ,12)
7.(9 ,13)
8.(10 ,14)
9.(15 ,16 ,17)
/
    iCD    cardinality /
$include GamsDat/Set_iCD.dat
/
    CarH(iCD,W)        /
$include GamsDat/Set_CarH.dat
/
    iCDT1  T1 cardinality   /
$include GamsDat/Set_iCDT1.dat
/
    CarT1( iCDT1, W )       /
$include GamsDat/Set_CarT1.dat
/
    iCDT   T1 cardinality  /
$include GamsDat/Set_iCDT.dat
/
    CarT( iCDT, W ) /
$include GamsDat/Set_CarT.dat
/
;

loop( (W,R1,R2)$WRR(W,R1,R2),  INr(R2,W) = yes;  OUr(R1,W) = yes; );
;

PARAMETERS
    H days                     /
$include GamsDat/Par_H.dat
/
    minBC min blend component      /
$include GamsDat/Par_minBC.dat
/
    maxBC min blend component   /
$include GamsDat/Par_maxBC.dat
/
    minN(iCD)   Cardinality     /
$include GamsDat/Par_minN.dat
/
    maxN(iCD)   Cardinality   /
$include GamsDat/Par_maxN.dat
/
    minN1(iCDT1) First slot cardinality  /
$include GamsDat/Par_minN1.dat
/
    maxN1(iCDT1) First slot cardinality  /
$include GamsDat/Par_maxN1.dat
/
    minNT(iCDT)  slot cardinality        /
$include GamsDat/Par_minNT.dat
/
    maxNT(iCDT)  Slot cardinality        /
$include GamsDat/Par_maxNT.dat
/
    FRL(W) flowrate limitations for transfer operation  /
$include GamsDat/Par_FRL.dat
/
    FRU(W) flowrate limitations for transfer operations /
$include GamsDat/Par_FRU.dat
/
    VL(W) operation batch vol LB /
$include GamsDat/Par_VL.dat
/
    VU(W) operation batch vol UB /
$include GamsDat/Par_VU.dat
/
    RVAT(RV)  vessel arrive time     /
$include GamsDat/Par_RVAT.dat
/
    RVLT(RV)  vessel leave time      /
$include GamsDat/Par_RVLT.dat
/
    TrTime(R) Transition Times after in operation  /
$include GamsDat/Par_TrTime.dat
/
    XL(WD,K) limits of property k of the blended products transfer/
$include GamsDat/Par_XL.dat
/
    XU(WD,K) limits of property k of the blended products transfer/
$include GamsDat/Par_XU.dat
/
    X(C,K) the vlaue of property k for crude c/
$include GamsDat/Par_X.dat
/
    TLL(R) capacity limits of tank /
$include GamsDat/Par_TLL.dat
/
    TLU(R) capacity limits of tank /
$include GamsDat/Par_TLU.dat
/
    TL0(R)  inital total level in tank k
    TCL0(R,C)  initial crude level in tank r for crude c /
$include GamsDat/Par_TCL0.dat
/
    CDUDL(RD) bounds of the CDU demand/
$include GamsDat/Par_CDUDL.dat
/
    CDUDU(RD) bounds of the CDU demand/
$include GamsDat/Par_CDUDU.dat
/
    G(C) Gross margin /
$include GamsDat/Par_G.dat
/
    DURL(W) duration limits /
$include GamsDat/Par_DURL.dat
/
    runOpTS(W) running oprations TS /
$include GamsDat/Par_runOpTS.dat
/
    runOpTE(W) running oprations TE /
$include GamsDat/Par_runOpTE.dat
/
    runOpV(W) running oprations Vol /
$include GamsDat/Par_runOpV.dat
/
    SL(WU) the minimum start time of unloading operation days
    TLHU(R) the max level of R at the end of H
    runOpRemainV(W)
    runOpRemainVC(W,C)
;

loop(R, TL0(R) = sum(c, TCL0(R,C)) );
loop(WU, SL(WU) = sum(RV$OUr(RV,WU), RVAT(RV) )  );
loop(W$(runOpTE(W)>0), runOpRemainV(W) = runOpV(W) * runOpTE(W) / (runOpTE(W)-runOpTS(W)) );

loop((W,C)$(runOpTE(W)>0), runOpRemainVC(W,C) = sum(R$(OUr(R,W) and TL0(R) > 0.0001 ), runOpRemainV(W) * TCL0(R,C) / TL0(R) ) ) ;

loop((W,RL,C)$(OUr(RL,W) and runOpTE(W)>0) , runOpRemainVC(W,C) = sum(W1$(INr(RL,W1)), runOpRemainVC(W1,C) )  );

*display  runOpRemainVC;

TLL(RV) = 0.0 ;   TLU(RV) = TL0(RV) ;    TLL(RL) = 0.0 ;   TLU(RL) = 0.0 ;
TLL(RD) = 0.0 ;   TLU(RD) = INF ;
TLHU(R) = TLU(R); TLHU(RV) = 0.0;
*display runOpRemainV;
binary variables
    Z(I,W) flag indicated operation w assigned to priority-slot T or not
;

positive variables
    S(I,W)   start time of operation W if assigned to priority-slot T
    D(I,W)   duration of operation w
    E(I,W)   end time of operation w
*    LTS(T,RL),LTE(T,RL)
    Vt(I,W)  total volume of crude transfered during operation W if assigned to priority-slot T
    Vc(I,W,C) volume of crude c transfered
    Lt(I,R)  total accumulated level of crude in tank TK before the operation assigned to priority-slot i
    Lc(I,R,C) accumulated level of crude c in tank TK
;

Z.fx('0',W) = 0; Z.fx('0',W)$(runOpTE(W)>0) =1;
S.fx('0',W) = max(0.0,runOpTS(W));
E.fx('0',W)   = runOpTE(W);
D.fx('0',W)   = runOpTE(W) - max(0.0,runOpTS(W));
Vt.fx('0',W)  = runOpRemainV(W);
Vc.fx('0',W,C) = runOpRemainVC(W,C);
Lt.fx('0',R)   = TL0(R);
Lc.fx('0',R,C) = TCL0(R,C);
Lt.lo('E',TK) = TLL(TK) ;   Lt.up('E',TK) = TLU(TK) ;   Lt.up('E',RV) = 0.0 ;
Lc.up('E',TK,C) = TLU(TK);  Lc.up('E',RV,C) = 0.0 ;
Lc.fx('E',RL,C) = 0.0;

S.up(T,W) = H;  E.up(T,W) = H;
loop((T,W,RV,R)$WRR(W,RV,R), E.up(T,W) = RVLT(RV); );
Vt.up(T,W) = VU(W);
Vc.up(T,W,C) = VU(W);
loop((T,W,RV,R,C)$WRR(W,RV,R), Vc.up(T,W,C)= TCL0(RV,C); );
Lt.lo(T,TK) = TLL(TK) ; Lt.up(T,TK) = TLU(TK) ;
Lc.up(T,TK,C) = TLU(TK);
Lc.up(T,RV,C) = TCL0(RV,C);
Lc.fx(T,RL,C) = 0.0;

variables
    fobj
;

EQUATIONS

EQOBJ
IEQSL(T,WU)
IEQEU(T,W)
EQSED(T,W)
IEQDURL(T,W)

Mincard(iCD)
MaxCard(iCD)
Mincard1(T,iCDT1)
MaxCard1(T,iCDT1)
MincardT(T,iCDT)
MaxCardT(T,iCDT)

EQPipeInGeOut(T,RL)

EQPipeInOutTSG(T,W1,W2,RL)
EQPipeInOutTSL(T,W1,W2,RL)
EQPipeInOutTEG(T,W1,W2,RL)
EQPipeInOutTEL(T,W1,W2,RL)

EBlenComL(T), EBlenComU(T)

IEQUnloadingTimePreced(RV1,RV2)
IEQUnloadingConst(T,RV1,RV2)
EQCDUNoInt(RD)
IEQVtUB(T,W)
IEQVtLB(T,W)
EQVtMB(T,W)
EQTankLevel(N,R)
EQTankCLevel(N,R,C)
EQTankMB(N,R)
IEQVtFLB(T,W)
IEQVtFUB(T,W)
IEQProdSpecLB(T,WD,K)
IEQProdSpecUB(T,WD,K)
EQCompMBNL(T,TK,W,C)

IEQLtLBLastV(T,R)
EQLtSumRC
EQCDUDemandLB(RD)
EQCDUDemandUB(RD)

IEQCliqueConst1(T,iCW)
IEQCliqueConst2(I1,I2,iCW),IEQCliqueTrTimeConst(I1,I2,R)
IEQSymBrkConst(T,W)
IEQNoEmptySlot(T,W)

;

EQOBJ..   fobj=e=sum((T,RD,W,C)$(INr(RD,W)),G(C)*Vc(T,W,C))
               + sum((RC,RD,W,C)$( WRR(W,RC,RD) and runOpRemainV(W)>0 ), G(C)* runOpRemainVC(W,C) ) ;

*----------------------------
IEQSL(T,WU)..   S(T,WU)=G=SL(WU)*Z(T,WU);
IEQEU(T,W)..    E(T,W)=L=H*Z(T,W);
EQSED(T,W)..    E(T,W)=E=S(T,W)+D(T,W);
IEQDURL(T,W)..  D(T,W)=G=Z(T,W)*DURL(W);

*--------------- cardinality constraints
Mincard(iCD)$(minN(iCD)>0)..       Sum((T,W)$CarH(iCD,W), Z(T,W)) =G= minN(iCD) ;
MaxCard(iCD)$(maxN(iCD)<INF)..     Sum((T,W)$CarH(iCD,W), Z(T,W)) =L= maxN(iCD) ;
Mincard1(T,iCDT1)$(ord(T)=1 And minN1(iCDT1)>0)..    Sum(W$CarT1(iCDT1,W), Z(T,W)) =G= minN1(iCDT1) ;
MaxCard1(T,iCDT1)$(ord(T)=1 And maxN1(iCDT1)<INF)..  Sum(W$CarT1(iCDT1,W), Z(T,W)) =L= maxN1(iCDT1) ;
MincardT(T,iCDT)$(minNT(iCDT)>0)..    Sum(W$CarT(iCDT,W), Z(T,W)) =G= minNT(iCDT) ;
MaxCardT(T,iCDT)$(maxNT(iCDT)<INF)..  Sum(W$CarT(iCDT,W), Z(T,W)) =L= maxNT(iCDT) ;

*---------------piple line constraints
EQPipeInGeOut(T,RL)..  sum( INr( RL,W), Z(T,W) ) =g= sum( OUr( RL,W), Z(T,W) ) ;

EQPipeInOutTSG(T,W1,W2,RL)$(INr(RL,W1) and OUr(RL,W2) )..  S(T,W1) - S(T,W2) =g=  - H * ( 2 - Z(T,W1) - Z(T,W2) )  ;
EQPipeInOutTSL(T,W1,W2,RL)$(INr(RL,W1) and OUr(RL,W2) )..  S(T,W1) - S(T,W2) =l=    H * ( 2 - Z(T,W1) - Z(T,W2) )  ;
EQPipeInOutTEG(T,W1,W2,RL)$(INr(RL,W1) and OUr(RL,W2) )..  E(T,W1) - E(T,W2) =g=  - H * ( 2 - Z(T,W1) - Z(T,W2) )  ;
EQPipeInOutTEL(T,W1,W2,RL)$(INr(RL,W1) and OUr(RL,W2) )..  E(T,W1) - E(T,W2) =l=    H * ( 2 - Z(T,W1) - Z(T,W2) )  ;

EBlenComL(T)..  Sum(W$INr('BL',W), Z(T,W)) =G= minBC * Sum(W$OUr('BL',W), Z(T,W)) ;
EBlenComU(T)..  Sum(W$INr('BL',W), Z(T,W)) =L= maxBC * Sum(W$OUr('BL',W), Z(T,W)) ;

*----------------unloading precedence constraints
IEQUnloadingTimePreced(RV1,RV2)$(ord(RV1)<ord(RV2) and TL0(RV1) >0 and TL0(RV2)>0 )..
                           sum((T,OUr(RV1,W)),E(T,W))=L=sum((T,OUr(RV2,W)),S(T,W));

IEQUnloadingConst(T,RV1,RV2)$(ord(RV1)<ord(RV2) and TL0(RV1) >0 and TL0(RV2)>0 )..
                           sum((T1,OUr(RV1,W))$(ord(T1)<ord(T)),Z(T1,W))=G=sum((T1,OUr(RV2,W))$(ord(T1)<=ord(T)),Z(T1,W));

*---------------CDUs must be operated without interruption
EQCDUNoInt(RD)..          sum((T,INr(RD,W)),D(T,W)) + sum(W$INr(RD,W), runOpTE(W) ) =E= H;

*-----------------transferring volume limits
IEQVtUB(T,W)..  Vt(T,W)=L=VU(W)*Z(T,W);
IEQVtLB(T,W)$(ord(T)<card(T))..  Vt(T,W)=G=VL(W)*Z(T,W);
EQVtMB(T,W)..    Vt(T,W) =E=sum(C,Vc(T,W,C));

*------------------tank level
EQTankLevel(N,R)..   Lt(N,R)=E=TL0(R)+ sum(W$INr(R,W), runOpRemainV(W) ) - sum(W$OUr(R,W), runOpRemainV(W) )
                                     + sum((N1,INr(R,W))$(ord(N1)<ord(N)),Vt(N1,W))-sum((N1,OUr(R,W))$(ord(N1)<ord(N)), Vt(N1,W));

EQTankCLevel(N,R,C)..  Lc(N,R,C)=E=TCL0(R,C) + sum((W)$(INr(R,W)and runOpRemainV(W)>0), runOpRemainVC(W,C) ) - sum(W$(OUr(R,W)and runOpRemainV(W)>0), runOpRemainVC(W,C) )
                                             + sum((N1,INr(R,W))$(ord(N1)<ord(N)),Vc(N1,W,C))-sum((N1,OUr(R,W))$(ord(N1)<ord(N)), Vc(N1,W,C));

EQTankMB(N,R)..      Lt(N,R)=E=sum(C,Lc(N,R,C));

*--------------------inventory capacity limitation
*** Last T Vt > VL
IEQLtLBLastV(T,R)$(ord(T)=card(T) and TLL(R)>0 )..    Lt(T,R)=G=TLL(R) + sum(W$OUr(R,W), VL(W)*Z(T,W) ) ;
EQLtSumRC..  sum(RC, Lt('E',RC) ) =g= VL('1') + sum(RC, TLL(RC) );


*------------------flowrate limitations that link volume and duration variables
IEQVtFLB(T,W)..    Vt(T,W)=G=FRL(W)*D(T,W);
IEQVtFUB(T,W)..    Vt(T,W)=L=FRU(W)*D(T,W);

*------------------product specifications
IEQProdSpecLB(T,WD,K)..   XL(WD,K)*Vt(T,WD)=L=sum(C,X(C,K)*Vc(T,WD,C));
IEQProdSpecUB(T,WD,K)..   XU(WD,K)*Vt(T,WD)=G=sum(C,X(C,K)*Vc(T,WD,C));

*------------------CDU demanding limitations
EQCDUDemandLB(RD)..      sum((T,INr(RD,WD)),Vt(T,WD)) + sum(W$INr(RD,W), runOpRemainV(W) ) =G= CDUDL(RD);
EQCDUDemandUB(RD)..      sum((T,INr(RD,WD)),Vt(T,WD)) + sum(W$INr(RD,W), runOpRemainV(W) ) =L= CDUDL(RD);

*-----------------strengthened constraints
IEQCliqueConst1(T,iCW)..  sum(W$CWW(iCW,W),Z(T,W)) =l= 1;

IEQCliqueConst2(I1,I2,iCW)$(ord(I1)<ord(I2) and ord(I2)<card(I) )..
                      sum(W$CWW(iCW,W),E(I1,W))  + sum((I,W)$(ord(I)>ord(I1) and ord(I)<ord(I2) and CWW(iCW,W) ),  D(I,W) ) =L=
                      sum(W$CWW(iCW,W),S(I2,W))  + H*(1- sum(W$CWW(iCW,W),Z(I2,W))) ;

IEQCliqueTrTimeConst(I1,I2,R)$(ord(I1)<ord(I2) and ord(I2)<card(I) and TrTime(R) > 0.0 )..
                      sum(W$INr(R,W),E(I1,W) + TrTime(R)*Z(I1,W) ) =L=
                      sum(W$OUr(R,W),S(I2,W))  + (H+TrTime(R))*(1- sum(W$OUr(R,W),Z(I2,W))) ;

*-------------symmetry-breaking constraints for MOS model
IEQSymBrkConst(T,W)$(ord(T)>1)..    Z(T,W)=L=sum(W1$(NOM(W,W1)),Z(T-1,W1)) + sum(W1$(NOM(W1,W)),Z(T-1,W1));

IEQNoEmptySlot(T,W)$(ord(T)>1)..   sum(W1,Z(T-1,W1))=G=Z(T,W);

*-----------------composition constraints : binlinear part
EQCompMBNL(T,TK,W,C)$(OUr(TK,W))..    Vc(T,W,C)*Lt(T,TK)=E=Lc(T,TK,C)*Vt(T,W);


Option MIP=CPLEX;
option optcr=0
MODEL BasicModel /
EQOBJ
EQSED
EQPipeInGeOut
EQPipeInOutTSG,EQPipeInOutTSL,EQPipeInOutTEG,EQPipeInOutTEL
EBlenComL,EBlenComU

IEQUnloadingTimePreced
EQCDUNoInt
EQVtMB
EQTankLevel
EQTankCLevel
IEQLtLBLastV , EQLtSumRC
EQTankMB
IEQVtFLB
IEQVtFUB
IEQProdSpecLB
IEQProdSpecUB

EQCDUDemandLB
EQCDUDemandUB
/
;

MODEL CrudeSchMILP /BasicModel
IEQSL,IEQEU,IEQDURL
******IEQSSeq
Mincard,MaxCard,Mincard1,MaxCard1,MincardT,MaxCardT
IEQUnloadingConst
IEQVtUB,IEQVtLB
IEQCliqueConst1
IEQCliqueConst2
IEQCliqueTrTimeConst
***IEQNoEmptySlot
/ ;

*MODEL CrudeSchMILP2 /CrudeSchMILP,
*IEQSymBrkConst
*/;


MODEL CrudeSchMINLP /CrudeSchMILP, EQCompMBNL/;

*$include CrudeSchMOS_CZ_Solve1.gms
$include CrudeSchMOS_CZ_SolveN.gms
$include CrudeScheMOS_CZ_PostSolve.gms

*** Check ***
Scalar valueTemp /0/
file  check / "check.csv" / ;
put check;
loop( (T,R,W,C)$(OUr(R,W)),
      valueTemp = Vc.l(T,W,C)*Lt.l(T,R) - Lc.l(T,R,C)*Vt.l(T,W) ;
     if( abs( valueTemp ) > 0.00001, put T.tl:0, ',', R.tl:0, ',', W.tl:0, ',',  C.tl:0, ',', valueTemp:0:4 /;  );
);

putclose check;
display fobj.l;

FILE schedule / ..\\Sol\\MOS_CZ_schedule.csv /;
PUT schedule;
loop((W,R1,R2)$(runOpTE(W)>0.0001 and WRR(W,R1,R2) ),
     put R1.tl:0, ',', R2.tl:0, ',', '0', ',', runOpTS(W):0:4, ',', runOpTE(W):0:4, ',', runOpV(W):0:4 /;
);
loop((W,R1,R2,T)$WRR(W,R1,R2),
     if(Z.l(T,W) > 0.9, put R1.tl:0, ',', R2.tl:0, ',', T.tl:0:0, ',', S.l(T,W):0:4, ',', E.l(T,W):0:4, ',', Vt.l(T,W):0:4 /; );
);
PUTCLOSE schedule;

FILE TankInv / ..\\Sol\\MOS_CZ_TankInv.csv /;
PUT TankInv;
LOOP(R,
   LOOP(Sol$(ord(Sol)<=nCount(R)),
      PUT R.tl:0, ',', ord(Sol):0, ',', fTime(R,Sol):0:4, ',' , fVal(R,Sol):0:4 /;
      if( ord(Sol) = nCount(R) and fTime(R,Sol) <> H , PUT R.tl:0, ',', ord(Sol):0, ',', H:0:4, ',' , fVal(R,Sol):0:4 /; );
   );
);
PUTCLOSE TankInv;










