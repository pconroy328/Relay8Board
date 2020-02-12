import logging
import RPi.GPIO as GPIO
import time
import json

class ChannelManager(object):

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        self.max_socket_num = 8
        self.socket_pin_assignments = {
            1: 2,
            2: 3,
            3: 4,
            4: 22,
            5: 10,
            6: 9,
            7: 27,
            8: 17}

        self.socket_states = {
            1: "unk",
            2: "unk",
            3: "unk",
            4: "unk",
            5: "unk",
            6: "unk",
            7: "unk",
            8: "unk"}

        self.socket_on_time = {
            1: 0.0,
            2: 0.0,
            3: 0.0,
            4: 0.0,
            5: 0.0,
            6: 0.0,
            7: 0.0,
            8: 0.0}

        self.socket_on_max_duration = {
            1: 0.0,
            2: 0.0,
            3: 0.0,
            4: 0.0,
            5: 0.0,
            6: 0.0,
            7: 0.0,
            8: 0.0}

        GPIO.setmode(GPIO.BCM)
        for key, value in self.socket_pin_assignments.items():
            logging.info( "Setting socket {} pin {} to GPIO Output".format(key,value))
            GPIO.setup(value, GPIO.OUT)
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def socket_on(self, socket_number,duration=900):
        if (socket_number <= 0 or socket_number > self.max_socket_num):
            logging.error( "Invalid socket number {} passed to the on command".format(socket_number))
            return

        pin_number = self.socket_pin_assignments[socket_number]
        logging.info('Sending on command to socket {} pin {}'.format(socket_number,pin_number))

        GPIO.output(pin_number,GPIO.LOW)
        self.socket_states[socket_number] = "on"
        self.socket_on_time[socket_number] = time.time()
        self.socket_on_max_duration[socket_number] = duration

    # ------------------------------------------------------------------------------------------------------------------
    def socket_off(self, socket_number):
        if (socket_number <= 0 or socket_number > self.max_socket_num):
            logging.error( "Invalid socket number {} passed to the off command".format(socket_number))
            return

        pin_number = self.socket_pin_assignments[socket_number]
        logging.info('Sending off command to socket {} pin {}'.format(socket_number,pin_number))

        GPIO.output(pin_number, GPIO.HIGH)
        self.socket_states[socket_number] = "off"
        self.socket_on_time[socket_number] = 0.0
        self.socket_on_max_duration[socket_number] = 0

    # ------------------------------------------------------------------------------------------------------------------
    def socket_all_on(self):
        logging.info('Sending on command to all sockets (default duration of 15 minutes)')
        for socket_number,pin_number in self.socket_pin_assignments.items():
            self.socket_on(socket_number,(15*60))

    # ------------------------------------------------------------------------------------------------------------------
    def socket_all_off(self):
        logging.info('Sending off command to all sockets')
        for socket_number,pin_number in self.socket_pin_assignments.items():
            self.socket_off(socket_number)

    # ------------------------------------------------------------------------------------------------------------------
    def check_for_duration_exceeded(self):
        logging.info('Checking for time exceeded on all on sockets')
        time_now = time.time()

        for socket_num,pin_number in self.socket_pin_assignments.items():
            if self.socket_states[socket_num] == 'on':
                max_seconds_on = self.socket_on_max_duration[socket_num]
                total_seconds_on = time_now - self.socket_on_time[socket_num]
                logging.debug('socket {} seconds on {} max_seconds_on {}'.format(socket_num,total_seconds_on,max_seconds_on))
                if (total_seconds_on > max_seconds_on):
                    logging.warning('Maximum On Time reached for socket {}. Sending off command'.format(socket_num))
                    self.socket_off(socket_num)

    # ------------------------------------------------------------------------------------------------------------------
    def status(self):
        logging.info('Returning status as JSON')

        c1 = { "channel" : 1, "state" : self.socket_states[1], "duration" : self.socket_on_max_duration[1] }
        c2 = { "channel" : 2, "state" : self.socket_states[2], "duration" : self.socket_on_max_duration[2] }
        c3 = { "channel" : 3, "state" : self.socket_states[3], "duration" : self.socket_on_max_duration[3] }
        c4 = { "channel" : 4, "state" : self.socket_states[4], "duration" : self.socket_on_max_duration[4] }

        c5 = { "channel" : 5, "state" : self.socket_states[5], "duration" : self.socket_on_max_duration[5] }
        c6 = { "channel" : 6, "state" : self.socket_states[6], "duration" : self.socket_on_max_duration[6] }
        c7 = { "channel" : 7, "state" : self.socket_states[7], "duration" : self.socket_on_max_duration[7] }
        c8 = { "channel" : 8, "state" : self.socket_states[8], "duration" : self.socket_on_max_duration[8] }

        states = [ c1, c2, c3, c4, c5, c6, c7, c8 ]
        #logging.info('All Channels {}'.format(states))
        return states
