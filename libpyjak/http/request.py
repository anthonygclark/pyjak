#!/usr/bin/python

class RequestHandler(object):
	request = None

	def __init__(self, request, *a, **kw):
		self.request = request


