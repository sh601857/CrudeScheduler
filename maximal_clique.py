import networkx as nx

#G=nx.Graph()

#G.add_nodes_from(range(1,8))
#G.add_edges_from([(1,3),(1,4),(2,5),(2,6),(3,7),(4,8) ,(5,7),(6,8),(7,8)])

#G.add_nodes_from(range(1,14))
#G.add_edges_from([(1,2),(1,3),(2,3),(1,4),(1,5),(2,6),(2,7),(2,8),(3,9),(3,10),(4,11),(6,11),(5,12),(5,13),(7,12),(9,12),(9,13),(8,14),(10,14),(12,13),(11,12),(13,14)])

#G.add_nodes_from(range(1,7))
#G.add_edges_from([(1,4),(1,5),(2,4),(2,6),(3,5),(3,6) ,(4,5),(4,6),(5,6)])

#G.add_nodes_from(range(1,17))
#G.add_edges_from([(1,2),(1,3),(1,4),(2,3),(2,5),(3,6),(7,11) ,(8,12),(9,13),(10,14),(15,16),(15,17),(16,17)])

#G.add_nodes_from(range(1,24))
#G.add_edges_from([(1,2), (1,6), (2,10), (3,4), (3,5), (3,7), (4,8),(5,9),
#(6,7),(6,8),(6,9),(6,10),(7,8),(7,9),(7,10),(8,9),(8,10),(9,10),
# (11,15),(11,19),(12,16),(12,20),(13,17),(13,21),(14,18),(14,22)])

G=nx.read_adjlist(r"D:\Workspace\Crude\CrudeScheduler\Set_NOM.dat", nodetype=int)

cliques=[clique for clique in nx.find_cliques(G)]
i=1
for clique in cliques:
     print( "{0}.(".format(i), end='')
     n=0
     for node in clique:
          if n==0:
               print( "{1}".format(i,node), end='')
          else:
               print( " ,{1}".format(i,node), end='')
          n=n+1

     print( ")" )
     i=i+1



     #import networkx as nx
     #from math import *
     #import matplotlib.pylab as plt
     #import itertools as it

     #def draw_circle_around_clique(clique,coords):
          #dist=0
          #temp_dist=0
          #center=[0 for i in range(2)]
          #color=colors.next()
          #for a in clique:
               #for b in clique:
                    #temp_dist=(coords[a][0]-coords[b][0])**2+(coords[a][1]-coords[b][2])**2
                    #if temp_dist>dist:
                    #dist=temp_dist
                    #for i in range(2):
                         #center[i]=(coords[a][i]+coords[b][i])/2
          #rad=dist**0.5/2
          #cir = plt.Circle((center[0],center[1]),   radius=rad*1.3,fill=False,color=color,hatch=hatches.next())
          #plt.gca().add_patch(cir)
          #plt.axis('scaled')
          ## return color of the circle, to use it as the color for vertices of the cliques
          #return color

     #global colors, hatches
     #colors=it.cycle('bgrcmyk')# blue, green, red, ...
     #hatches=it.cycle('/\|-+*')

     ## create a random graph
     #G=nx.gnp_random_graph(n=7,p=0.6)
     ## remember the coordinates of the vertices
     #coords=nx.spring_layout(G)

     ## remove "len(clique)>2" if you're interested in maxcliques with 2 edges
     #cliques=[clique for clique in nx.find_cliques(G) if len(clique)>2]

     ##draw the graph
     #nx.draw(G,pos=coords)
     #for clique in cliques:
          #print ("Clique to appear: ",clique)
     #nx.draw_networkx_nodes(G,pos=coords,nodelist=clique,node_color=draw_circle_around_clique(clique,coords))

     #plt.show()