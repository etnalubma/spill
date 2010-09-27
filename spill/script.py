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
from subprocess import call
from spill.formatter import PlanHelpFormatter
from spill.utils import run_editor, get_uptime


try:
    import simplejson as json
except ImportError:
    import json


def signal_handler(signal, frame):
        print '\n Cobarde!'
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

parser = optparse.OptionParser(
    prog='./spill.py',
    formatter=PlainHelpFormatter(),
    description=u'''
    /     \
    vvvvvvv  /|__/|
       I   /O,O   |
       I /_____   |      /|/|
      J|/^ ^ ^ \  |    /00  |    _//|
       |^ ^ ^ ^ |W|   |/^^\ |   /oo |
        \m___m__|_|    \m_m_|   \mm_|
    ''',
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


def do_spill():
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
        tempfile = tempfile.NamedTemporaryFile()
        message = run_editor(tempfile.name)

        if message == '' or message == '\n':
            print('Message is blank, so is your mind, Press ^C to exit')
            description = "".join(sys.stdin.readlines())
        else:
            description = message

    values = dict(
        author=args[0].author,
        description=description,
        tags=args[0].tags,
        metadata={
            'uptime': get_uptime(),
        },
    )

    print "Connecting to %s/%s ..." % (server, path)

    headers = {"Content-Type": "application/json"}
    conn = httplib.HTTPConnection(server)
    conn.request("POST", "/" + path, json.dumps(values), headers)
    response = conn.getresponse()
    print response.status, response.reason
    print response.read()
    conn.close()
