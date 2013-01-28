#!/usr/bin/python

from protocol import ProtocolUDP
from protocol import ProtocolTCP

def register(config, reactor):
	if 'udp' in config.mpi_protocol:
		ProtocolUDP.activate(reactor)
	if 'tcp' in config.mpi_protocol:
		ProtocolTCP.activate(reactor)

