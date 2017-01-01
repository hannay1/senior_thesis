#!/bin/bash

OUTPUT_INTERFACE="eth0"
AP_INTERFACE="wlan0"
MON_INTERFACE="wlan1mon"
AP_NAME="ITSFreeWifi"
DHCPDCONF="/etc/dhcpd.conf"

echo "Configuring at0...."
ifconfig at0 up
ifconfig at0 mtu 1800
ifconfig at0 192.168.3.1 netmask 255.255.255.0
echo "adding routes..."
route add -net 192.168.3.0 netmask 255.255.255.0 gw 192.168.3.1
iptables -P FORWARD ACCEPT
iptables --append FORWARD --in-interface at0 -j ACCEPT
iptables -t nat -A POSTROUTING -o "$OUTPUT_INTERFACE" -j MASQUERADE
sleep 3;
echo "setting routing options/IP forwarding..."
iptables -t nat -A PREROUTING -p tcp -i at0 --destination-port 80 -j REDIRECT --to-port 8080
iptables -t nat -A PREROUTING -p tcp -i at0 --destination-port 443 -j REDIRECT --to-port 8080
sleep 3;
sysctl -w net.ipv4.ip_forward=1
echo "1" > /proc/sys/net/ipv4/ip_forward
echo "clearing leases & starting dhcpd server..."
echo > '/var/lib/dhcp/dhcpd.leases'
dhcpd -d -f -cf "$DHCPDCONF" at0
