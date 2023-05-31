from pysnmp.hlapi import *
from tabulate import tabulate
from interface import Interface
from router import Router
from easysnmp import Session
from routing_tables_poller import RoutingTablesPoller
from routeSummaries import RouteSummaries

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
    networks = []
    next_hop = []
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
        
        # Create an SNMP session
        session = Session(hostname=ip, community=community, version=2)
        RTP = RoutingTablesPoller(ip, community, session)
        # Get the routing tables info
        networks2, masks, next_hop2, type_link = RTP.getRoutingTablesInfo()
        networks.extend(networks2)
        next_hop.extend(next_hop2)
        
        RS = RouteSummaries()
        RS.createSummaries(networks, next_hop)

# Call the main function when the script is executed (DEVELOPMENT ONLY)
if __name__ == "__main__":
    main()