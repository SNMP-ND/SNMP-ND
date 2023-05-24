from pysnmp.hlapi import *

def snmpwalk(host, community, oid):
    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in nextCmd(SnmpEngine(),
                               CommunityData(community),
                               UdpTransportTarget((host, 161)),
                               ContextData(),
                               ObjectType(ObjectIdentity(oid))):
        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                print(' = '.join([x.prettyPrint() for x in varBind]))

snmpwalk('11.0.0.2', 'public', '.1.3.6.1.2.1.1')
