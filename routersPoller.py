from pysnmp.hlapi import *

start_router = '11.0.0.2'
community = 'public'

routers_to_poll = [start_router]

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

        
    
    