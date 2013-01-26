#!/usr/bin/python

# Our server model is inspired partly by:
# https://github.com/twisted/klein/blob/master/klein/app.py
# https://github.com/twisted/klein/blob/master/klein/resource.py

from twisted.web import server, resource, error
from twisted.python import log
from twisted.internet import reactor, defer
import sys, re


HANDLERS = []
SERVER_STRING = 'Pyjak HTTP v0.01'

def route(regex, handler):
	global HANDLERS
	if isinstance(handler, RequestHandler):
		handlers.append((regex, handler))


class RequestHandler(object):
	request = None


class PyjakResource(resource.Resource):
	isLeaf = True

	@staticmethod
	def construct_fullpath(request): # Produce the original URI path as a single string
		prepath, postpath = None, None
		if request.prepath:
			prepat = '/' + '/'.join(request.prepath)
		if request.postpath:
			postpath = '/' + '/'.join(request.postpath)
		return (prepath or '') + (postpath or '')


	def render(self, request):
		global HANDLERS

		request.setHeader('Server', SERVER_STRING)
		deferreds = []

		# Collect common request mapping context
		server_name = request.getRequestHostname()
		server_port = request.getHost().port
		is_secure = request.isSecure()
		fullpath = self.construct_fullpath(request)
		url_scheme = is_secure and 'https' or 'http'
	
		# Update server_name if a port number is required
		if (int(is_secure), server_port) not in [ (1, 443), (0, 80) ]:
			server_name = '%s:%d' % (server_name, server_port)
		
		def _cleanup(err):
			del deferreds[:]

		def _coersion(result): # Ensure that values coming from the handlers have usable formats, etc
			# TODO: support other deferred types here, e.g. templates, JSON rendering, etc
			if isinstance(result, basestring):
				if isinstance(result, unicode):
					result = result.encode('utf-8')
				request.write(res)
			request.finish()

		request.notifyFinish().addCallback(_cleanup) # cleanup

		handler_count = 0
		for regex, handler in HANDLERS:
			handler_count = handler_count +1
			handler.request = request
			m = re.match(regex, fullpath)
			x = getattr(handler, request.method.lower(), None)
			if m and x:
				args = m.groups()
				kwargs = m.groupdict()
				_deferred = defer.maybeDeferred(x, *args, **kwargs)
				_deferred.addErrback(request.processingFailed)
				_deferred.addCallback(_coersion)
				deferreds.append(_deferred)
				
				res = x(*(m.groups()), **(m.groupdict())) # Call the handler's matching method
		

		if handler_count is 0:
			return resource.NoResource().render(request)
		else:
			return server.NOT_DONE_YET


def run(host = None, port = 8080, logfile = None):
	logfile = logfile or sys.stdout
	log.startLogging(logfile)
	reactor.listenTCP(port, server.Site(PyjakResource()), interface = host or '0.0.0.0')
	reactor.run()


if __name__ == '__main__':
	run()
