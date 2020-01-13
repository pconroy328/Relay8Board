#
# Program to control the 8 Channel Relay Board
# 13Jan2020 Patrick Conroy
# pip3 install paho.mqtt
#
import _thread
import time
import paho.mqtt.client as mqtt
import logging


# ------------------------------------------------------------------------------
# function to listen to the MQTT broker for commands
def on_message_received():
    logging.INFO("MQTT Message Received")
    pass


# ------------------------------------------------------------------------------
def main():
    broker_address = 'localhost'

    logging.basicConfig(filename='/tmp/relay8_1.log', level=logging.INFO)
    client = mqtt.Client(client_id='relay8_1', clean_session=True, userdata=None)
    logging.info("Connecting to the MQTT Broker on {}".format(broker_address))
    try:
        client.connect(broker_address)
        client.on_message = on_message_received
        client.subscribe('RELAY/1/CMD')

    except:
        logging.critical("Unable to connect to the MQTT broker on {}".format(broker_address))
    pass


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    main()

