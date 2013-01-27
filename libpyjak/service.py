#!/usr/bin/py

from twisted.internet import reactor
from twisted.python import log

from http import server as http_server
from mpi import server as mpi_server

import config
import sys

def run(conf = None):
	conf = conf or config.load()
	logfile = conf.logfile and open(conf.logfile, 'wb') or sys.stdout
	log.startLogging(logfile)
	http_server.register(conf, reactor)
	mpi_server.register(conf, reactor)
	reactor.run()
