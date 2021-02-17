pellets
==============================
A wrapper around pika to facilitate sending and receiving RabbitMQ messages


Usage
=============================
from pellets import DurableMessenger

msgr = DurableMessenger.DurableMessenger('/path/to/creds/broker_creds.crypt')
conn = msgr.get_conn()
msgr.make_channel(conn, <CHANNEL_NAME>)
if listen:
    msgr.listen(<CHANNEL_NAME>)
else:
    msgr.send_message(conn, <CHANNEL_NAME>, <MSG>)
msgr.close_conn(conn)


Installation
=============================
pip install pellets


Requirements
=============================
pika
cryptography


Compatibility
=============================
Python 3.9


License
=============================
GNU GPL v3.0


Authors
=============================
pellets was written by James parks <james_parks@hotmail.com>

