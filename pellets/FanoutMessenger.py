#!/usr/bin/env python

import os
import sys
import json
import datetime
import subprocess
from optparse import OptionParser

import pika

from BaseMessenger import *


def parse_args(all_args):
    parser = OptionParser(version = '%prog 1.0')
    parser.add_option('-l', '--listen', action='store_true', help='enter listen mode')

    options, args = parser.parse_args(all_args)
    return options, args


class FanoutMessenger(BaseMessenger):
    def talk_make_channel(self, conn, exch_name):
        channel = conn.channel()
        channel.exchange_declare(exchange=exch_name, exchange_type='fanout')
        return channel 

    def listen_make_channel(self, conn, exch_name):
        channel = conn.channel()
        channel.exchange_declare(exchange=exch_name, exchange_type='fanout')
        res = channel.queue_declare(exclusive=True)
        queue_name = res.method.queue
        channel.queue_bind(exchange=exch_name, queue=queue_name)
        return channel, queue_name

    def send_message(self, conn, exch_name, msg):
        chan = self.talk_make_channel(conn, exch_name)
        chan.basic_publish(exchange=exch_name, routing_key='', body=msg, properties=pika.BasicProperties(delivery_mode = 2)) # make message persistent
        print(' [x] Sent "{}"'.format(msg))

    def callback(self, ch, method, properties, body):
        print(' [x] Fanout Received {}'.format(body))

    def listen(self, exch_name):
        chan, queue_name = self.listen_make_channel(self.conn, exch_name)
        chan.basic_consume(self.callback, queue=queue_name, no_ack=True)
        print(' [*] Waiting for messages, CTRL+C to exit')
        chan.start_consuming()


if __name__ == '__main__':
    options, args = parse_args(sys.argv[1:])
    my_msgr = FanoutMessenger()
    my_conn = my_msgr.get_conn()
    if options.listen:
        #my_chan = my_msgr.listen_make_channel(my_conn, 'fanout_test')
        my_msgr.listen('fanout_test')
    else:
        #my_chan = my_msgr.talk_make_channel(my_conn, 'fanout_test')
        my_msgr.send_message(my_conn, 'fanout_test', 'Fanout at {}'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S')))
    my_msgr.close_conn(my_conn)



