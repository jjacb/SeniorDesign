#!/bin/bash
#This script automatically gets the host ip address of the pi connected
#via the ethernet port and uses it to set up the stream to that pi

#Make sure you have the following package
#sudo apt-get install gawk

#IPADDRESS=$(ifconfig eth0| grep 'inet addr:' | cut -d: -f2 | awk '{print $1}')
IPADDRESS=10.0.0.20
raspivid -t 0 -h 480 -w 640 -fps 15 -hf -b 2000000 -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=5 pt=96 ! udpsink host=$IPADDRESS port=5003



 


