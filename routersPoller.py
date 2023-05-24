from pysnmp.hlapi import *
from tabulate import tabulate

start_router = '11.0.0.2'
community = 'public'

routers_to_poll = [start_router]
routing_table = []

for router in routers_to_poll:
    # First, get the system name
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(community),
               UdpTransportTarget((router, 161)),
               ContextData(),
               ObjectType(ObjectIdentity('1.3.6.1.2.1.1.5.0')))
    )
    
    if errorIndication or errorStatus:
        print('SNMP request error:', errorIndication or errorStatus)
        continue

    sysName = varBinds[0][1]
    print(f'System Name for {router}: {sysName}')

    max_neighbors = 3
    neighbors_retrieved = 0

    # Next, get the OSPF neighbors
    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in nextCmd(SnmpEngine(),
                               CommunityData(community),
                               UdpTransportTarget((router, 161)),
                               ContextData(),
                               ObjectType(ObjectIdentity('1.3.6.1.2.1.14.10.1.1'))):  # OID for ospfNbrIpAddr
        
        if errorIndication or errorStatus:
            print('SNMP request error:', errorIndication or errorStatus)
            break

        ospf_neighbor = str(varBinds[0])
        ospf_neighbor = str(ospf_neighbor[ospf_neighbor.find("=")+2:])
        print(f'Ospf Neighbor for {router}: {ospf_neighbor}')

        if ospf_neighbor in routers_to_poll:
            break

        if ospf_neighbor not in routers_to_poll:
            routers_to_poll.append(ospf_neighbor)


    interfaces_retrieved = 0
    max_int = 3

    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in nextCmd(SnmpEngine(),
                        CommunityData(community),
                        UdpTransportTarget((router, 161)),
                        ContextData(),
                        ObjectType(ObjectIdentity('IF-MIB', 'ifIndex')),
                        ObjectType(ObjectIdentity('IF-MIB', 'ifDescr')),
                        ObjectType(ObjectIdentity('IF-MIB', 'ifOperStatus')),
                        ObjectType(ObjectIdentity('IF-MIB', 'ifSpeed')),
                        ObjectType(ObjectIdentity('IP-MIB', 'ipAdEntIfIndex')),
                        ):
        
        if errorIndication or errorStatus:
            print('SNMP request error:', errorIndication or errorStatus)
            break

        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))

        interfaces_retrieved+=1

        if max_int >= max_neighbors:
            break
    
    max_tables = 8
    done = 0

    routing_table_oid = '1.3.6.1.2.1.4.21'  # OID for the routing table
    destination_oid = '1.3.6.1.2.1.4.21.1.1'  # OID for destination
    route_type_oid = '1.3.6.1.2.1.4.21.1.8'  # OID for route type
    next_hop_oid = '1.3.6.1.2.1.4.21.1.7'  # OID for next hop
    interface_oid = '1.3.6.1.2.1.4.21.1.2'  # OID for interface

    for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(
            SnmpEngine(),
            CommunityData(community),
            UdpTransportTarget((router, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(destination_oid)),
            ObjectType(ObjectIdentity(route_type_oid)),
            ObjectType(ObjectIdentity(next_hop_oid)),
            ObjectType(ObjectIdentity(interface_oid))):

        if errorIndication or errorStatus:
            print('SNMP request error:', errorIndication or errorStatus)
            break
        for varBind in varBinds:
            routing_table_entry = [x.prettyPrint() for x in varBind]
            routing_table.append(routing_table_entry)

        done+=1
        if done >= max_tables:
            break

    headers = ["Destination", "Route Type", "Next Hop", "Interface"]

    # Print the routing table using the tabulate library
    print(tabulate(routing_table, headers=headers, tablefmt="grid"))


        
    
    