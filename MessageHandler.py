import logging
import json
import datetime
import sys
import paho.mqtt.client as mqtt
from ChannelManager import ChannelManager

class MessageHandler(object):

    def __init__(self, broker_address="mqtt.local"):
        # self.local_broker_address = ''
        self.broker_address = broker_address
        self.client = mqtt.Client(client_id="", clean_session=True, userdata=None)
        self.channel_manager = ChannelManager()
        self.subscription_topic = 'RELAY/#'

    # ---------------------------------------------------------------------
    def on_connect(self, client, userdata, flags, rc):
        logging.info('Connected to the MQTT broker!')
        pass

    # ---------------------------------------------------------------------
    def on_message(self, client, userdata, message):
        logging.debug('Message has arrived')
        payload = str(message.payload.decode("utf-8"))
        try:
            jsonPayload = json.loads(payload)
            msgTopic = str.upper(jsonPayload['topic'])
            msgTopicParts = msgTopic.split('/')

            if msgTopicParts[2] == 'CMD':
                relayID = str.upper(jsonPayload['id'])
                channel = jsonPayload['channel']
                command = str.upper(jsonPayload['command'])
                duration = jsonPayload['duration']
                logging.debug('Command came in for relay {}, command {}, channel {}, duration {}'.format(msgTopicParts[1],command,channel,duration))

                if command == 'ON':
                    self.channel_manager.socket_on(channel,duration)
                elif command == 'OFF':
                    self.channel_manager.socket_off(channel)
                elif command == 'ALLON':
                    self.channel_manager.socket_all_on()
                elif command == 'ALLOFF':
                    self.channel_manager.socket_all_off()
                else:
                    logging.error('Unrecognized command in message {}. Payload {}'.format(command, jsonPayload))
            else:
                pass
        except Exception:
            logging.exception('Exception hit in decoding message')
            pass

    # ---------------------------------------------------------------------
    def start(self):
        logging.info('Message handling start - v4')
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        print('Start - connecting to ', self.broker_address)
        try:
            self.client.connect(self.broker_address)
            self.client.subscribe(self.subscription_topic,0)
            self.client.loop_start()
        except Exception:
            logging.exception('Exception hit trying to connect to MQTT broker {}'.format(self.broker_address))
            logging.critical('Exiting on exception hit trying to connect to MQTT broker {}'.format(self.broker_address))
            sys.exit(1)

    # ---------------------------------------------------------------------
    def cleanup(self):
        self.client.unsubscribe(self.subscription_topic,0)
        self.client.disconnect()
        self.client.loop_stop()

    # ---------------------------------------------------------------------
    def send_status_info(self):
        logging.debug('Sending relay status info!')
        try:
            data = {}
            data['topic'] = 'RELAY/RV8.1/STATUS'
            data['datetime'] = datetime.datetime.now().replace(microsecond=0).isoformat()
            data['id'] = 'RV8.1'
            data['states'] = self.channel_manager.status()

            json_data = json.dumps(data)

            logging.debug('Final status as JSON {}'.format(json_data))
            self.client.publish(data['topic'], json_data, qos=0)
        except Exception:
            logging.exception('Exception in sending status info')

    # ---------------------------------------------------------------------
    def check_for_duration_exceeded(self):
        self.channel_manager.check_for_duration_exceeded()
