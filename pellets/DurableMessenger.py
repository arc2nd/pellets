#!/usr/bin/env python
import os
import sys
import json
import datetime
import subprocess
from optparse import OptionParser

import pika

from .BaseMessenger import *


def parse_args(all_args):
    parser = OptionParser(version = '%prog 1.0')
    parser.add_option('-l', '--listen', action='store_true', help='enter listen mode')

    options, args = parser.parse_args(all_args)
    return options, args


class DurableMessenger(BaseMessenger):
    def make_channel(self, conn, chan_name):
        channel = conn.channel()
        channel.queue_declare(queue=chan_name, durable=True)
        return channel

    def send_message(self, conn, chan_name, msg):
        chan = self.make_channel(conn, chan_name)
        chan.basic_publish(exchange='', routing_key=chan_name, body=msg, properties=pika.BasicProperties(delivery_mode = 2)) # make message persistent
        print(' [x] Sent "{}"'.format(msg))

    def callback(self, ch, method, properties, body):
        print(' [x] Received {}'.format(body))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def listen(self, chan_name):
        chan = self.make_channel(self.conn, chan_name)
        chan.basic_qos(prefetch_count=1)
        chan.basic_consume(self.callback, queue=chan_name)
        print(' [*] Waiting for messages, CTRL+C to exit')
        chan.start_consuming()



if __name__ == '__main__':
    options, args = parse_args(sys.argv[1:])
    my_msgr = DurableMessenger()
    my_conn = my_msgr.get_conn()
    my_chan = my_msgr.make_channel(my_conn, 'durable_test')
    if options.listen:
        my_msgr.listen('durable_test')
    else:
        my_msgr.send_message(my_conn, 'durable_test', 'Durable at {}'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S')))
    my_msgr.close_conn(my_conn)


