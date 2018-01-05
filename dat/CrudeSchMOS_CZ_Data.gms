$onempty
Option Limrow=0;
Option Limcol=0;
Option Solprint=off;

SETS
    W     /1*17
$include GamsDat/Set_preOp.dat
/
    WU(W) /15*17/
    WT(W) /4*14 /
    WD(W) /1*3/
    R     /V1,V2,V3, G181*G184, G101*G102,G109,TL,BL,CDU1/
    TK(R)    tanks         /G181*G184,G101*G102,G109/
    RV(R)    vessels       /V1,V2,V3/
    RC(TK)   charging tank /G101*G102,G109/
    RD(R)    CDU           /CDU1 /
    RL(R)    Pipeline      /TL,BL  /
    INr(R,W)
    OUr(R,W)
;
ALIAS(W,W1,W2);
ALIAS(R,R1,R2);
ALIAS(RV,RV1,RV2);

SETS
    NOM(W1,W2)   non-overlapping matrix  /
$include GamsDat/Par_preOpNOM.dat
/
    WRR(W,R1,R2) Operations and Units   /
$include GamsDat/Set_WRR.dat
/
;

loop( (W,R1,R2)$WRR(W,R1,R2),  INr(R2,W) = yes;  OUr(R1,W) = yes; );
*loop( (W,RD)$INr(RD,W),  WD(W) = yes; );
*display WD
;
*** Forbit tank in and out at the same time slot
loop( (TK,W1,W2)$(INr(TK,W1) and OUr(TK,W2) and ord(W1)<ord(W2) ),  NOM( W1,W2) = yes; )
loop( (TK,W1,W2)$(OUr(TK,W1) and INr(TK,W2) and ord(W1)<ord(W2) ),  NOM( W1,W2) = yes; )
*** only one CDU in at the same slot
loop( (RD,W1,W2)$(INr(RD,W1) and INr(RD,W2) and ord(W1)<ord(W2) ),  NOM( W1,W2) = yes; )
*** only one out at the same slot
*loop( (R,W1,W2)$(OUr(R,W1) and OUr(R,W2) and ord(W1)<ord(W2) ),  NOM( W1,W2) = yes; )
*** one vessel at a time slot
loop( (RV1,RV2,W1,W2)$(OUr(RV1,W1) and OUr(RV2,W2) and ord(RV1)<ord(RV2) ),  NOM( W1,W2) = yes; )

FILE NOM_Put / GamsDat\\Set_NOM.txt/;
*NOM_Put.ap = 1;
PUT NOM_Put;
loop( W1,
    loop( W2$NOM(W1,W2),
         put W1.tl:0, ' ',  W2.tl:0  /;
*        put '(', W1.tl:0, ',',  W2.tl:0 ,'),' ;
    );
*    put /;
);
PUTCLOSE NOM_Put;

FILE NOM_Put_dat / GamsDat\\Set_NOM.dat/;
PUT NOM_Put_dat;
loop( W1,
    loop( W2$NOM(W1,W2),
         put W1.tl:0, '.',  W2.tl:0  /;
*        put '(', W1.tl:0, ',',  W2.tl:0 ,'),' ;
    );
*    put /;
);
PUTCLOSE NOM_Put_dat;

Execute '=python "MaximalClique.py" '


