#!/bin/bash

IFACE=${1:-wlan0}

# switch to ad-hoc mode
iwconfig ${IFACE} mode ad-hoc

# set the channel/frequence
iwconfig ${IFACE} channel 7

# add ssid
iwconfig ${IFACE} essid 'cndc11'

# add WEP encryption
iwconfig ${IFACE} key 12345689

# Adcivation
ip link set ${IFACE} up

# start dhclient / static?
# dhclient ${IFACE}
ip addr add 192.168.7.7/24 dev ${IFACE}




