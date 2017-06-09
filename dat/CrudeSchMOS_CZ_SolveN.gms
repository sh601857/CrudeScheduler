Option MIP=CPLEX;
CrudeSchMILP.optfile=1;
option optcr=0
Solve  CrudeSchMILP  maximizing fobj using MIP;

set soln           possible solutions in the solution pool /file1*file10/
    solnpool(soln) actual solutions;
file fsol;

parameters
bestsoln / -1 /
bestObj  / -INF /
solnObj(soln);
option savepoint=2
execute_load 'solnpool.gdx', solnpool=Index;
loop(solnpool(soln),
    put_utility fsol 'gdxin' / solnpool.te(soln):0:0;
    execute_loadpoint;

    S.up(T,W) = H;  E.up(T,W) = H;  D.up(T,W)=H;
    loop((T,W,RV,R)$WRR(W,RV,R), E.up(T,W) = RVLT(RV); );
    Vt.up(T,W)   = VU(W);
    Vc.up(T,W,C) = VU(W);
    loop((T,W,RV,R,C)$WRR(W,RV,R), Vc.up(T,W,C)= TCL0(RV,C); );

    Z.fx(T,W) = Z.l(T,W);
    loop((T,W)$( Z.l(T,W) < 0.5 ),  S.fx(T,W)=0.0 ; D.fx(T,W)=0.0 ; E.fx(T,W)=0.0;
        Vt.fx(T,W)=0.0; Vc.fx(T,W,C)=0.0;
    );
    Solve CrudeSchMINLP maximizing fobj using RMINLP ;
    if( CrudeSchMINLP.modelStat < 3 ,
        solnObj(soln) =  fobj.l;
        if( bestObj < fobj.l ,
            bestObj = fobj.l; bestsoln = ord(soln);
*            put_utility 'gdxout' / solnpool.te(soln):0:0;
*            execute_unload D,E,fobj,Lc,Lt,S,Vc,Vt,Z;
        );
    );
);
display  bestsoln,solnObj;

put_utility fsol 'gdxin' / 'CrudeSchMINLP_p':0:0, bestsoln:0:0, '.gdx':0:0 ;
execute_loadpoint;
