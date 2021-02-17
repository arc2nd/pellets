#!/usr/bin/env python
import os
import sys
import json
import datetime
import subprocess
from optparse import OptionParser

import pika


def parse_args(all_args):
    parser = OptionParser(version = '%prog 1.0')
    parser.add_option('-l', '--listen', action='store_true', help='enter listen mode')

    options, args = parser.parse_args(all_args)
    return options, args


class BaseMessenger(object):
    def __init__(self, path='creds/broker_creds.crypt'):
        self.creds = None
        self.get_creds(path)
        self.conn = self.get_conn()

    def get_creds(self, path):
        try:
            import crypto as crypto
        except ModuleNotFoundError:
            import pellets.crypto as crypto
        self.creds = crypto.get_creds(path)

    def get_creds_old(self, path):
        j = None
        cmd = "openssl des3 -salt -d -in %s -pass pass:%s" % (path, os.path.basename(path))
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output = proc.communicate()[0]
        if (output):
            try:
                j = json.loads(output)
            except:
                j = None
        return j

    def get_conn(self):
        local_creds = pika.PlainCredentials(self.creds['USER'], self.creds['PASS'])
        if isinstance(local_creds, pika.PlainCredentials):
            conn = pika.BlockingConnection(pika.ConnectionParameters(self.creds['SERVER'], self.creds['PORT'], '/', local_creds))
            return conn

    def make_channel(self, conn, chan_name):
        channel = conn.channel()
        channel.queue_declare(queue=chan_name)
        return channel

    def send_message(self, conn, chan_name, msg):
        chan = self.make_channel(conn, chan_name)
        chan.basic_publish(exchange='', routing_key=chan_name, body=msg)
        print(' [x] Sent "{}"'.format(msg))

    def close_conn(self, conn):
        conn.close()

    def callback(self, ch, method, properties, body):
        print(' [x] Received {}'.format(body))

    def listen(self, chan_name):
        chan = self.make_channel(self.conn, chan_name)
        # chan.basic_consume(self.callback, queue=chan_name, no_ack=True)
        chan.basic_consumer(queue=chan_name, on_message_callback=self.callback, auto_ack=True)
        print(' [*] Waiting for messages, CTRL+C to exit')
        chan.start_consuming()


if __name__ == '__main__':
    options, args = parse_args(sys.argv[1:])
    chan_name = 'baseTestTopic'
    msgr = BaseMessenger('/mnt/creds/broker_creds.crypt')
    conn = msgr.get_conn()
    chan = msgr.make_channel(my_conn, chan_name)
    if options.listen:
        msgr.listen(chan_name)
    else:
        msgr.send_message(conn, chan_name, 'Base at {}'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S')))
    msgr.close_conn(conn)



