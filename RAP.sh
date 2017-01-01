#!/bin/bash

OUTPUT_INTERFACE="eth0"
AP_INTERFACE="wlan0"
MON_INTERFACE="wlan0mon"
AP_NAME="ItsFreeWifi"
DHCPDCONF="/etc/dhcpd.conf"


if [ "$1" == "start" ]
        then
                echo "starting access point..."
                sleep 1;
                echo "***Putting card into monitor mode...***"
                airmon-ng start "$AP_INTERFACE"
                sleep 8;
                echo "Setting up access point..."
                airbase-ng -e "$AP_NAME" "$MON_INTERFACE"
                sleep 8;
elif [ "$1" == "stop" ]
        then
                echo "killing airbase..."
                pkill airbase-ng
                sleep 4;
                echo "killing dhcpd..."
                pkill dhcpd
                rm /var/run/dhcpd.pid
                sleep 3;
                echo "flushing iptables..."
                sleep 1;
                sudo iptables --flush && iptables --table nat --flush && iptables --delete-chain && iptables --table nat --delete-chain
                echo "disabling IP forwarding..."
                echo "0" > /proc/sys/net/ipv4/ip_forward
                echo "stopping airmon-ng"
                airmon-ng stop "$MON_INTERFACE"
                sleep 2;
else 
        echo "plz respond properly"
fi
