#!/usr/bin/python

from twisted.internet.protocol import DatagramProtocol # UDP
from twisted.internet.protocol import Protocol # TCP

# Reference: UDP = http://twistedmatrix.com/documents/12.2.0/core/howto/udp.html
# Reference: TCP = http://twistedmatrix.com/documents/12.2.0/core/howto/servers.html

class PyjakProtocol(object):
	@classmethod
	def activate(cls, reactor):
		pass


class ProtocolUDP(PyjakProtocol, DatagramProtocol):
	pass

class ProtocolTCP(PyjakProtocol, Protocol):
	pass
