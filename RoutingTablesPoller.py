from easysnmp import Session
from tabulate import tabulate

ROUTE_NETWORK_OID = '1.3.6.1.2.1.4.24.4.1.1'  # OID for network
ROUTE_MASK_OID = '1.3.6.1.2.1.4.24.4.1.2'  # OID for mask
ROUTE_NEXT_HOP_OID = '1.3.6.1.2.1.4.24.4.1.4'  # OID for next hop
ROUTE_TYPE_OID = '1.3.6.1.2.1.4.24.4.1.8'  # OID for route type

class RoutingTablesPoller:
    router = None
    community = None
    session = None
    networks = None
    masks = None
    next_hop = None
    type_link = None
    route_type = None
    def __init__(self, router, community, session):
        self.router = router
        self.community = community
        self.session = session


    def print_table(self, networks, masks, next_hop, route_type):
            table_data = []

            for net, mask, hop, link in zip(networks, masks, next_hop, route_type):
                table_data.append([net, mask, hop, link])

            # Define the headers for the table
            headers = ["Network", "Mask", "Next Hop", "Type of Link"]

            # Print the table using the tabulate library
            print(tabulate(table_data, headers=headers, tablefmt="grid"))


    def getRoutingTablesInfo(self):
        networks = list(map(lambda x: x.value, self.session.walk(ROUTE_NETWORK_OID)))
        masks = list(map(lambda x: x.value, self.session.walk(ROUTE_MASK_OID)))
        next_hop = list(map(lambda x: x.value, self.session.walk(ROUTE_NEXT_HOP_OID)))
        route_type = list(map(lambda x: x.value, self.session.walk(ROUTE_TYPE_OID)))

        self.print_table(networks, masks, next_hop, route_type)
        
        return networks, masks, next_hop, route_type

    