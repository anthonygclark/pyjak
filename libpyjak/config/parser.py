#!/usr/bin/python

# This is the configuration module for Pyjak.
# It reads arguments from command line and integrates them with
# options from a configuration file.

from ConfigParser import ConfigParser
from optparse import OptionParser
import sys, os

# TODO: support Python 3 via the argparse model

# Default network name.
# Cluster nodes will inquire with all directors available via broadcast,
# and then register with any directors participating in the same network
# by name.
CLUSTER_NETWORK_DEFAULT = 'pyjak'

# Where should server logs go?
LOGFILE_DEFAULT = '/var/log/pyjak.log'

def _options(origin):
	parser = OptionParser()
	parser.add_option('-f', '--config', dest = 'configfile', help = 'Configuration file')
	parser.add_option('-l', '--logfile', dest = 'logfile', help = 'Log output file')
	parser.add_option('-D', '--director', dest = 'director_mode', action = 'store_true', help = 'Activate Director mode')
	parser.add_option('-W', '--worker', dest = 'worker_mode', action = 'store_true', help = 'Activate Worker mode')
	parser.add_option('-N', '--network', dest = 'cluster_network', action = 'append', help = 'Join a cluster network by name') 
	return parser.parse_args(origin)




class PyjakConfig(object):

	# HTTP defaults
	http_host = '0.0.0.0'
	http_port = 8080
	
	# MPI defaults 
	mpi_host = '0.0.0.0'
	mpi_port = 1629
	mpi_protocol = [ 'tcp' ]

	
	director_network = []
	worker_network = []

	def __init__(self, origin):
		# Read options from command line first
		options, args = _options(origin)
	
		_network = (options.cluster_network or len(options.cluster_network)) and options.cluster_network or [ CLUSTER_NETWORK_DEFAULT ]
		
		if options.director_mode:
			self.director_network.extend(_network)

		if options.worker_mode:
			self.worker_network.extend(_network)

		self.logfile = options.logfile or LOGFILE_DEFAULT

		self.mode = options.mode or 'worker' # default

		# Read options from config file
		if options.configfile and os.path.isfile(options.configfile):
			config = ConfigParser()
			config.read(options.configfile)
		
			for k, v in config.items('Daemon'):
				if k == 'http_port':
					self.http_port = int(v)
				if k == 'http_host':
					self.http_host = v
				if k == 'mpi_port':
					self.mpi_port = int(v)
				if k == 'mpi_host':
					self.mpi_host = v
				if k == 'mpi_protocol':
					self.mpi_protocol = v.replace('both', 'tcp,udp').split(',')

	
		
		


def load(origin = None):
	if isinstance(origin, basestring):
		import shlex
		origin = shlex.split(origin)
	elif origin is None:
		origin = sys.argv

	return PyjakConfig(origin)

