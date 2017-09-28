

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img=mpimg.imread("resources\Textures\dweller.JPG")
# draw graph without images
G =nx.Graph()
G.add_edge(0,1,image=img,size=0.1)
G.add_edge(0,6,image=img,size=0.1)
G.add_edge(0,7,image=img,size=0.1)
G.add_edge(1,2,image=img,size=0.1)
G.add_edge(2,3,image=img,size=0.1)
G.add_edge(3,4,image=img,size=0.1)
G.add_edge(3,5,image=img,size=0.1)
labelsOfVerticies = {i : str(i) for i in range(8)}

pos=nx.spring_layout(G)
print pos


# add images on edges
ax=plt.gca()
fig=plt.gcf()

label_pos = 0.5 # middle of edge, halfway between nodes
ax_transData = ax.transData.transform
fig_invtrans = fig.transFigure.inverted().transform
imsize = 0.1 # this is the image size
nx.draw(G,pos)

for (n1,n2) in G.edges():
    (x1,y1) = pos[n1]
    (x2,y2) = pos[n2]

    (x,y) = (x1 * label_pos + x2 * (1.0 - label_pos), y1 * label_pos + y2 * (1.0 - label_pos)) # weighted average

    xx,yy = ax_transData((x, y)) # figure coordinates
    xa,ya = fig_invtrans((xx, yy)) # axes coordinates

    a = plt.axes([xa-imsize/2.0,ya-imsize/2.0, imsize, imsize])

    print "n1 = ", n1, pos[n1], "n2 = ", n2, pos[n2], "xx", xx, "yy", yy, "xa", xa, "ya", ya
    img =  G[n1][n2]['image']
    a.imshow(img)
    plt.xlabel(str(n1) + "-" + str(n2))
    plt.ylabel(str(n1) + "-" + str(n2))
    # a.set_aspect('equal')
    # a.axis('off')

nx.draw_networkx_labels(G, pos, labelsOfVerticies, ax = ax)

plt.savefig('resources\sysFiles\graphFiles\simple.png')
plt.show()