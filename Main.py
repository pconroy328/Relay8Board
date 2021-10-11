#########################################
## Tring to fix picking up the Roomba MQTT broker
#########################################

import logging
from zeroconf import ServiceBrowser, Zeroconf
import time
import sys
from MessageHandler import MessageHandler
import socket


def discover_mqtt_host():
    from zeroconf import ServiceBrowser, Zeroconf
    host = None
    info = None

    def on_service_state_change(zeroconf, service_type, name, state_change):
        pass

    my_zeroconf = Zeroconf()
    browser = ServiceBrowser(my_zeroconf, "_mqtt._tcp.local.",
                             handlers=[on_service_state_change])
    i = 0
    while not host:
        time.sleep(0.1)
        if browser.services:
            service = list(browser.services.values())[0]
            info = my_zeroconf.get_service_info(service.name, service.alias)
            ##print('info', info)
            ##print('info.server', info.server)
            host = socket.inet_ntoa(info.address)
        i += 1
        if i > 50:
            break
    my_zeroconf.close()
    try:
        return info.server, host
    except AttributeError:
        return None

# ----------------------------------------------------------------------------------------------------------------------
version='v0.1.3 roomba - passing in MQTT broker'
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='/tmp/relay8rv.log')
logging.warning('Relay8rv starting. Version {}'.format(version))

try:
   host = sys.argv[1]
   mqtt_broker_address = sys.argv[1]
except:
   print( 'No host passed in on command line. Trying mDNS' )
   logging.info('Multicast DNS Service Discovery started')
   host = discover_mqtt_host()
   if (host is not None):
       mqtt_broker_address = host[0]
       logging.info( 'Found MQTT Broker using mDNS on {}.{}'.format(host[0], host[1]))
   else:
       logging.warning('Unable to locate MQTT Broker using DNS')
       try:
           mqtt_broker_address = sys.argv[1]
       except:
           logging.critical('mDNS failed and no MQTT Broker address passed in via command line. Exiting')
           sys.exit(1)

logging.debug('Connecting to {}'.format(mqtt_broker_address))
m = MessageHandler(broker_address=mqtt_broker_address)
m.start()

loop_count = 0
while True:
    m.check_for_duration_exceeded()
    time.sleep(5)

    loop_count += 1
    # Send a status every minute
    if (loop_count % (60 / 5) == 0):
        m.send_status_info()
        loop_count = 0
