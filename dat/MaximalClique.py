
import networkx as nx

G=nx.read_adjlist(u"GamsDat\\Set_NOM.txt", nodetype=int)
file_Set_CWW = open(u'GamsDat\\Set_CWW.dat', 'w')
file_Set_iCW = open(u'GamsDat\\Set_iCW.dat', 'w')

cliques=[clique for clique in nx.find_cliques(G)]
i=1
for clique in cliques:
     file_Set_CWW.write( "{0}.(".format(i))
     n=0
     for node in clique:
          if n==0:
               file_Set_CWW.write( "{1}".format(i,node))
          else:
               file_Set_CWW.write( " ,{1}".format(i,node))
          n=n+1

     file_Set_CWW.write( ")\n" )
     i=i+1
file_Set_iCW.write( "1*{0}".format(i-1) )
	 
file_Set_CWW.close()
file_Set_iCW.close()