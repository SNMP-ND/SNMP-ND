from pysnmp.hlapi import *
from tabulate import tabulate
from interface import Interface
from router import Router

snmpEngine = SnmpEngine()
routers = []

# DEVELOPMENT ENVIRONMENT VARIABLES
knownIP = '11.0.0.2'
community = 'public'

IPsToPoll = [knownIP]
routingTable = []

def getSysName(ip : str):
    errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(snmpEngine,
                CommunityData(community),
                UdpTransportTarget((ip, 161)),
                ContextData(),
                ObjectType(ObjectIdentity('1.3.6.1.2.1.1.5.0')))
        )
        
    if errorIndication or errorStatus:
        print('SNMP request error:', errorIndication or errorStatus)

    return varBinds[0][1]

def getOSPFNeighbors(ip : str):
    neighbors = []
    for (errorIndication,
            errorStatus,
            errorIndex,
            varBinds) in nextCmd(snmpEngine,
                                CommunityData(community),
                                UdpTransportTarget((ip, 161)),
                                ContextData(),
                                ObjectType(ObjectIdentity('1.3.6.1.2.1.14.10.1.1'))):  # OID for ospfNbrIpAddr
            
            if errorIndication or errorStatus:
                print('SNMP request error:', errorIndication or errorStatus)
                break

            ospfNeighbor = str(varBinds[0])
            ospfNeighbor = str(ospfNeighbor[ospfNeighbor.find("=")+2:])

            # Check for avoiding duplicates or infinite loops
            if ospfNeighbor in IPsToPoll or ospfNeighbor == '0':
                break
            else:
                IPsToPoll.append(ospfNeighbor)
                neighbors.append(ospfNeighbor)
            
    return neighbors
    
def getInterfaces(ip : str):
    interfacesIndexesRetrieved = []
    interfaces = []
    for (errorIndication,
            errorStatus,
            errorIndex,
            varBinds) in nextCmd(snmpEngine,
                            CommunityData(community),
                            UdpTransportTarget((ip, 161)),
                            ContextData(),
                            ObjectType(ObjectIdentity('IF-MIB', 'ifIndex')),
                            ObjectType(ObjectIdentity('IF-MIB', 'ifDescr')),
                            ObjectType(ObjectIdentity('IF-MIB', 'ifOperStatus')),
                            ObjectType(ObjectIdentity('IF-MIB', 'ifSpeed')),
                            ObjectType(ObjectIdentity('IP-MIB', 'ipAdEntAddr')),
                            ):
            
            if errorIndication or errorStatus:
                print('SNMP request error:', errorIndication or errorStatus)
                break

            # Extract the interface information from the varBinds
            ifIndex = varBinds[0][1]
            idDescr = varBinds[1][1]
            ifOperStatus = varBinds[2][1]
            ifSpeed = varBinds[3][1]
            ipAdEntAddr = str(varBinds[4]).split("= ")[1]

            # Create a new interface object
            interface = Interface(ifIndex, idDescr, ifOperStatus, ifSpeed, ipAdEntAddr)

            # Check for avoiding duplicates or infinite loops
            if ifIndex not in interfacesIndexesRetrieved:
                interfacesIndexesRetrieved.append(ifIndex)
                interfaces.append(interface)
            else:
                break
    return interfaces


def main():
    for ip in IPsToPoll:

        # First, get the system name

        sysName = getSysName(ip)
        router = Router(sysName)

        # Next, get the OSPF neighbors
        neighbors = getOSPFNeighbors(ip)
        router.setNeighbors(neighbors)

        # Next, get the interfaces
        interfaces = getInterfaces(ip)
        router.setInterfaces(interfaces)

        # Prints for debugging
        print("Router: " + router.getSysName())
        print("Neighbors: " + str(router.getNeighbors()))
        print("Interfaces:")
        for interface in router.getInterfaces():
            print(interface)
        
        max_tables = 8
        done = 0

        destination_oid = '1.3.6.1.2.1.4.21.1.1'  # OID for destination
        route_type_oid = '1.3.6.1.2.1.4.21.1.8'  # OID for route type
        next_hop_oid = '1.3.6.1.2.1.4.21.1.7'  # OID for next hop
        interface_oid = '1.3.6.1.2.1.4.21.1.2'  # OID for interface
        routing_table_oid = '1.3.6.1.2.1.4.21'

        ROUTE_NETWORK_OID = "IP-FORWARD-MIB::ipCidrRouteDest"
        ROUTE_MASK_OID = "IP-FORWARD-MIB::ipCidrRouteMask"
        ROUTE_NEXT_HOP_OID = "IP-FORWARD-MIB::ipCidrRouteNextHop"
        ROUTE_TYPE_OID = "IP-FORWARD-MIB::ipCidrRouteType"


        routingTable = []  # List to store routing table entries

        # SNMP walk operation
        for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(
                SnmpEngine(),
                CommunityData(community),
                UdpTransportTarget((ip, 161)),
                ContextData(),
                ObjectType(ObjectIdentity('IP-FORWARD-MIB', 'ipCidrRouteDest')),
                ObjectType(ObjectIdentity('IP-FORWARD-MIB', 'ipCidrRouteNextHop')),
                ObjectType(ObjectIdentity('IP-FORWARD-MIB', 'ipCidrRouteType'))
        ):
            if errorIndication:
                print(f'SNMP Error: {errorIndication}')
                break
            elif errorStatus:
                print(f'SNMP Error: {errorStatus.prettyPrint()}')
                break
            else:
                # Process the varBinds for routing table information
                for varBind in varBinds:
                    print(varBind)
                    # Data treat
        # Print the routing table using the tabulate library


# Call the main function when the script is executed (DEVELOPMENT ONLY)
if __name__ == "__main__":
    main()