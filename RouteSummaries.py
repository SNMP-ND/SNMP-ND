from netaddr import IPNetwork
import networkx as nx
import itertools


class RouteSummaries:

    def createSummaries(self, networksR, next_hopR):
        networks = networksR
        next_hop = next_hopR
        print("Creating summaries...")
        print("Networks: " + str(networks))
        print("Next hop: " + str(next_hop))
        
        G = nx.Graph()

        # Add nodes to the graph
        for net, hop in zip(networks, next_hop):
            G.add_node(net, next_hop=hop)

        for pair in itertools.combinations(networks, 2):
            src_net, dst_net = pair

            # Calculate the shortest path between the source and destination networks
            try:
                shortest_path = nx.shortest_path(G, src_net, dst_net)
                src_hop = G.nodes[src_net]['next_hop']
                dst_hop = G.nodes[dst_net]['next_hop']

                print(f"IPorig: {src_hop} -> {' -> '.join(shortest_path)} -> IPdest: {dst_hop}")
            except nx.NetworkXNoPath:
                pass


