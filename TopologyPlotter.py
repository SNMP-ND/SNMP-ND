import networkx as nx
import matplotlib.pyplot as plt


class TopologyPlotter:
    routers: list

    def __init__(self, routers: list):
        self.routers = routers
    
    def plotTopology(self):
        G = nx.Graph()
        for router in self.routers:
            G.add_node(router.getSysName())
            neighbors = router.getNeighbors()
            for neighbor in neighbors:
                G.add_edge(router.getSysName(), neighbor)
        nx.draw(G, with_labels=True)
        plt.show()