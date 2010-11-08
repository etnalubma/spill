#!/usr/bin/env python
# -*- coding: utf-8 -*-
import optparse
import httplib
import urllib
import sys
import os
import signal
import tempfile
import getpass

from spill.formatter import PlainHelpFormatter
from spill.utils import run_editor, get_uptime


try:
    import simplejson as json
except ImportError:
    import json


def signal_handler(signal, frame):
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

parser = optparse.OptionParser(
    prog='./spill.py',
    formatter=PlainHelpFormatter(),
    epilog='''
        Las cucarachas lograron con exito su plan, echando a los pestilentes
        sangre caliente de sus cajas de cemento. Ahora el hombre es una especie
        errante en el espacio, un vagabundo errante en las estrellas.'''
    )

parser.add_option(
   '-m',
   '--message',
   metavar='TEXT',
   default=None,
   help='the message to send to the site, reads from stdin if None'
)

parser.add_option(
   '-t',
   '--tags',
   metavar='TAG,[TAG,...]',
   type="string",
   default="r,",
   help='tags associated to the message'
)
parser.add_option(
   '-a',
   '--author',
   metavar='NAME',
   type="string",
   default=os.getlogin(),
   help='author associated to the message, not to be confused with source'
)
parser.add_option(
   '-s',
   '--source',
   metavar='NAME',
   type="string",
   default='ROBADO',
   help='source associated to the message, not to be confused with author'
)

parser.add_option(
   '-r',
   '--remote-server',
   metavar='HOST:PORT[/PATH]',
   type="string",
   default="ltmo.com.ar/",
   help='destination HOST, PORT and PATH of server, useful for debugging'
)


def process_args():

    args = parser.parse_args()

    remote = args[0].remote_server.split("/")
    server = remote[0]
    if len(remote) > 1:
        path = "/".join(remote[1:])
    else:
        path = ""

    if args[0].message:
        description = args[0].message
    else:
        tmpfile = tempfile.NamedTemporaryFile()
        message = run_editor(tmpfile.name)

        if message == '' or message == '\n':
            print('Message is blank, so is your mind,\nPress ^C to exit')
            description = "".join(sys.stdin.readlines())
        else:
            description = message

    return {
            'author': args[0].author,
            'description': description,
            'tags': args[0].tags,
            'server': server,
            'path': path,
            'metadata': {
                'uptime': get_uptime(),
                },
            }


def do_spill():

    arguments = process_args()
    path = arguments['path']
    server = arguments['server']
    print "Connecting to %s/%s ..." % (server, path)
    headers = {"Content-Type": "application/json"}
    conn = httplib.HTTPConnection(server)
    conn.request("POST", "/" + path, json.dumps(arguments), headers)
    response = conn.getresponse()
    print response.status, response.reason
    print response.read()
    conn.close()

if __name__ == '__main__':
    do_spill()
