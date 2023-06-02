import networkx as nx
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import math

class TopologyPlotter:
    routers: list

    def __init__(self, routers: list):
        self.routers = routers
    
    def plotTopology(self):
        G = nx.Graph()
        for router in self.routers:

            G.add_node(router.getSysName())

            for neighbor in router.getNeighbors():

                router1Interfaces = router.getInterfaces()
                router2Interfaces = neighbor.getInterfaces()

                for interface1 in router1Interfaces:
                    for interface2 in router2Interfaces:

                        if (interface1.isLinkedWith(interface2)):
                            label = interface1.getIP() + "-" + interface2.getIP() + " " + str(int(min(interface1.getSpeed(), interface2.getSpeed()))/1000000) + "Gbps"
                            G.add_edge(router.getSysName(), neighbor.getSysName(), label=label)
                            break
                
        pos = nx.spring_layout(G)
        
        plt.figure(figsize=(12, 8))
        node_size = 1000
        node_color = "darkblue"
        font_color = "white"
        edge_color = "gray"
        node_shape = "s"  # Use square shape for nodes
        node_style = nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=node_color, edgecolors="black", linewidths=1, node_shape=node_shape)
        node_style.set_edgecolor("black")

        edge_style = nx.draw_networkx_edges(G, pos, edge_color=edge_color, width=1.5, alpha=0.7)

        nx.draw_networkx_labels(G, pos, font_color=font_color, font_size=10, font_weight="bold")

        edge_labels = nx.get_edge_attributes(G, 'label')
        for edge, label in edge_labels.items():
            x = (pos[edge[0]][0] + pos[edge[1]][0]) / 2  # Calculate x-coordinate for label position
            y = (pos[edge[0]][1] + pos[edge[1]][1]) / 2 + 0.1  # Calculate y-coordinate for label position
            plt.text(x, y, label, horizontalalignment='center', verticalalignment='center', fontsize=8)

        plt.axis("off")
        plt.show()