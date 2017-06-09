SETS
   Sol /Sol1*Sol20/
;

PARAMETERS
   fTime(R,Sol)
   fVal(R,Sol)
   nCount(R)
;

SCALARS
   fobj1,fobj2,nIndex,fLastDif,fTemp,nPos,bFlag,nStart,nEnd,nNum;
;
nIndex=0;
fVal(R,Sol)=0;
LOOP(R,
   nIndex=1;
   fTime(R,'Sol1')=0;
   fVal(R,'Sol1')=TL0(R);
*************************************************************************
   LOOP(W$((INr(R,W) or OUr(R,W)) and (runOpTE(W)>0)),
       nPos=nIndex;
       bFlag=0;
       while(nPos>0 and bFlag=0,
           fTemp=sum(Sol$(ord(Sol)=nPos),fTime(R,Sol));
           if(runOpTE(W)>fTemp,
               nNum=nIndex;
               WHILE(nNum>nPos,
                   fTime(R,Sol+1)$(ord(Sol)=nNum)=fTime(R,Sol);
                   nNum=nNum-1;
               );
               fTime(R,Sol)$(ord(Sol)=nPos+1)=runOpTE(W);
               nIndex=nIndex+1;
               bFlag=1;
            elseif(runOpTE(W)<fTemp),
               nPos=nPos-1;
            else
               bFlag=1;
            );
        );
   );
***************************************************************************
   LOOP(T,
      LOOP(W$((INr(R,W) or OUr(R,W)) and (E.l(T,W)>0)),
          if(S.l(T,W)>0,
                  nPos=nIndex;
                  bFlag=0;
                  while(nPos>0 and bFlag=0,
                      fTemp=sum(Sol$(ord(Sol)=nPos),fTime(R,Sol));
                      if(S.l(T,W)>fTemp,
                         nNum=nIndex;
                         WHILE(nNum>nPos,
                             fTime(R,Sol+1)$(ord(Sol)=nNum)=fTime(R,Sol);
                             nNum=nNum-1;
                         );
                         fTime(R,Sol)$(ord(Sol)=nPos+1)=S.l(T,W);
                         nIndex=nIndex+1;
                         bFlag=1;
                      elseif(S.l(T,W)<fTemp),
                         nPos=nPos-1;
                      else
                         bFlag=1;
                      );
                  );
          );
          nPos=nIndex;
          bFlag=0;
          while(nPos>0 and bFlag=0,
              fTemp=sum(Sol$(ord(Sol)=nPos),fTime(R,Sol));
              nNum=nIndex;
              if(E.l(T,W)>fTemp,
                 WHILE(nNum>nPos,
                    fTime(R,Sol+1)$(ord(Sol)=nNum)=fTime(R,Sol);
                    nNum=nNum-1;
                 );
                 fTime(R,Sol)$(ord(Sol)=nPos+1)=E.l(T,W);
                 nIndex=nIndex+1;
                 bFlag=1;
              elseif(E.l(T,W)<fTemp),
                 nPos=nPos-1;
              else
                 bFlag=1;
              );
          );
      );
   );
   nCount(R)=nIndex;
**************************************************
       LOOP(W$((INr(R,W) or OUr(R,W)) and (runOpTE(W)>0) ),
          nPos=1;
          bFlag=0;
          while(nPos<=nCount(R) and bFlag=0,
               fTemp=sum(Sol$(ord(Sol)=nPos),fTime(R,Sol));
               if(runOpTE(W)=fTemp,
                  nEnd=nPos;
                  bFlag=1;
               else
                  nPos=nPos+1;
               );
          );
          fTemp$(INr(R,W))= runOpRemainV(W) / runOpTE(W);
          fTemp$(OUr(R,W))=-runOpRemainV(W) / runOpTE(W);
          if(ord(R)=1,
               display fTemp;
          );
          nIndex=1;
          while(nIndex<nEnd,
                LOOP(Sol$(ord(Sol)=nIndex+1),
                   fVal(R,Sol)=fVal(R,Sol)+fTemp*(fTime(R,Sol)-fTime(R,Sol-1));
                );
                nIndex=nIndex+1;
          );
      );
*******************************************************
   LOOP(T,
      LOOP(W$((INr(R,W) or OUr(R,W)) and (E.l(T,W)>0)),
          nPos=1;
          bFlag=0;
          while(nPos<=nCount(R) and bFlag=0,
               fTemp=sum(Sol$(ord(Sol)=nPos),fTime(R,Sol));
               if(S.l(T,W)=fTemp,
                  nStart=nPos;
                  bFlag=1;
               else
                  nPos=nPos+1;
               );
          );
          nPos=1;
          bFlag=0;
          while(nPos<=nCount(R) and bFlag=0,
               fTemp=sum(Sol$(ord(Sol)=nPos),fTime(R,Sol));
               if(E.l(T,W)=fTemp,
                  nEnd=nPos;
                  bFlag=1;
               else
                  nPos=nPos+1;
               );
          );
          fTemp$(INr(R,W))=Vt.l(T,W)/(E.l(T,W)-S.l(T,W));
          fTemp$(OUr(R,W))=-Vt.l(T,W)/(E.l(T,W)-S.l(T,W));
          if(ord(R)=1,
               display fTemp;
          );
          nIndex=nStart;
          while(nIndex<nEnd,
                LOOP(Sol$(ord(Sol)=nIndex+1),
                   fVal(R,Sol)=fVal(R,Sol)+fTemp*(fTime(R,Sol)-fTime(R,Sol-1));
                );
                nIndex=nIndex+1;
          );
      );
   );

   LOOP(Sol$(ord(Sol)>1),
       fVal(R,Sol)=fVal(R,Sol-1)+fVal(R,Sol);
   );
);

display fTime,fVal;
