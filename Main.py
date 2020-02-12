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
version='v0.0.1'
logging.basicConfig(filename='/tmp/relay8rv.log', level=logging.DEBUG)
logging.warning('Relay8rv starting. Version {}'.format(version))

logging.info('Multicast DNS Service Discovery started')
hostData = discover_mqtt_host()
if (hostData is not None):
    mqtt_broker_address = hostData[0]
    logging.info( 'Found MQTT Broker using mDNS on {}.{}'.format(hostData[0], hostData[1]))
else:
    logging.warning('Unable to locate MQTT Broker using mDNS. Checking for command line argument')
    try:
        mqtt_broker_address = sys.argv[1]
    except:
        logging.critical('No MQTT Broker address passed in via command line')
        sys.exit(1)

logging.debug('Connecting to {}'.format(mqtt_broker_address))
m = MessageHandler(broker_address=mqtt_broker_address)
m.start()

while True:
    m.check_for_duration_exceeded()
    time.sleep(5)
