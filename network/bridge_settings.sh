#!/bin/bash

BR=$(brctl show | grep '^br0 *')
if [ -z "$BR" ]; then
    sudo brctl addbr br0
    sudo ip a a 192.168.1.1/24 dev br0
    sudo iptables -A FORWARD -i br0 -s 192.168.1.0/255.255.255.0 -j ACCEPT
    sudo iptables -A FORWARD -i eth0 -d 192.168.1.0/255.255.255.0 -j ACCEPT
    sudo iptables -t nat -I POSTROUTING -o eth0 -j MASQUERADE
    sudo ifconfig br0 up
fi
