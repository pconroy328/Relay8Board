#!/bin/bash
#   1: 2, 2: 3, 3: 4, 4: 22,
#   5: 10, 6: 9, 7: 27, 8: 17}
#
mqtthost=$1
if test -z "$mqtthost" 
then
      mqtthost=mqttrv.local
fi

# How Long
duration=$2

command=on
socket=6
pin=9
dt=`date -Iseconds`

message="{ \"topic\":\"RELAY/RV8.1/CMD\",\"datetime\":\"${dt}\",\"id\":\"RV8.1\",\"channel\":$socket,\"command\":\"${command}\",\"duration\":${duration} }"

mosquitto_pub -h ${mqtthost} -t "RELAY/RV8.1/CMD" -m "$message"
status=$?

if test $status -eq 0
then
	echo "Socket ${socket} should be on via MQTT on host ${mqtthost}"
else
	echo "MQTT comamnd to turn on Socket ${socket} failed - using direct method"
	gpio -g mode ${pin} output
	gpio -g write ${pin} 0
fi

