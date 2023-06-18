#!/bin/sh

while read line; do

    first_part=$(echo "$line" | cut -d ' ' -f 1)
    second_part=$(echo "$line" | cut -d ' ' -f 2)

    if [ "$first_part" = "iso.3.6.1.2.1.14.1.1" ]; then
        echo " ------------------------------------------------- ">> /var/log/snmptraps.log
        echo "| Trap from $second_part received                     |" >> /var/log/snmptraps.log
    fi

    if [ "$first_part" = "iso.3.6.1.2.1.14.10.1.1" ]; then
        echo "| OSPF neighbor with ip $second_part has changed state |" >> /var/log/snmptraps.log
        echo " ------------------------------------------------- " >> /var/log/snmptraps.log
    fi
done