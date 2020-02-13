#!/bin/bash
#   1: 2, 2: 3, 3: 4, 4: 22,
#   5: 10, 6: 9, 7: 27, 8: 17}
#

##
## MQTT Host is option command line parameter #1
## If not used, we'll default to the named MQTT RV broker
mqtthost=$1
if test -z "$mqtthost" 
then
      mqtthost=mqttrv.local
fi

##
## Set Command, socket and pin number
command=on
socket=6
pin=9

##
## For On Commands only, the on duration in seconds is parameter #2
## If not used, we'll default to 1800 seconds (30 mins)
duration=$2
if test -z "$duration"
then
	duration=1800
fi

##
## Get the date/time now in ISO8601 format
dt=`date -Iseconds`

##
## Craft the MQTT Message
message="{ \"topic\":\"RELAY/RV8.1/CMD\",\"datetime\":\"${dt}\",\"id\":\"RV8.1\",\"channel\":$socket,\"command\":\"${command}\",\"duration\":${duration} }"

##
## Publish the message
mosquitto_pub -h ${mqtthost} -t "RELAY/RV8.1/CMD" -m "$message"
status=$?

if test $status -eq 0
then
	echo "Socket ${socket} should be ${command} via MQTT on host ${mqtthost}"
else
        # If the MQTT way fails, try to use the GPIO utility
	echo "MQTT comamnd to turn ${command} Socket ${socket} failed - using direct method"
	gpio -g mode ${pin} output
	gpio -g write ${pin} 0
fi

