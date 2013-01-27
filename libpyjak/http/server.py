#!/usr/bin/python

# Our server model is inspired partly by:
# https://github.com/twisted/klein/blob/master/klein/app.py
# https://github.com/twisted/klein/blob/master/klein/resource.py

from twisted.web import server, resource, error
from twisted.python import log
from twisted.internet import reactor, defer

from http.request import RequestHandler
import sys, re



HANDLERS = []
SERVER_STRING = 'Pyjak HTTP v0.01'
SERVER_TIMEOUT = 3 # seconds

class TimeoutResource(resource.ErrorPage):
	code = 408
	brief = 'This response timed out.'
	detail = 'A useful response was not generated in time. Sorry.'



class PyjakResource(resource.Resource):
	isLeaf = True # the buck stops here.
	_registered_routes = []

	@staticmethod
	def construct_fullpath(request): # Produce the original URI path as a single string
		prepath, postpath = None, None
		if request.prepath:
			prepat = '/' + '/'.join(request.prepath)
		if request.postpath:
			postpath = '/' + '/'.join(request.postpath)
		return (prepath or '') + (postpath or '')

	@classmethod
	def route(cls, handler, regex, *a, **kw):
		if issubclass(handler, RequestHandler):
			cls._registered_routes.append((handler, re.compile(regex), a, kw))
		else:
			raise Exception('Invalid request handler')


	@classmethod # get the first matching configured route, or None
	def findroute(cls, name = None, path = None, method = None, scheme = None, secure = False, request = None, _routes = None):
		_routes = _routes or cls._registered_routes # allow override
		for handler, regex, args, kwargs in _routes:
			res = re.match(regex, path)
			if res and method and callable(getattr(handler, method, None)):
				return res, handler( request, # construct the handler
						_host = name, 
						_path = path, 
						_method = method,
						_scheme = scheme,
						_secure = secure
					) 
		return None, None


	def render(self, request):
		request.setHeader('Server', SERVER_STRING)

		# Collect common request mapping context
		server_name = request.getRequestHostname()
		server_port = request.getHost().port
		is_secure = request.isSecure()
		fullpath = self.construct_fullpath(request)
		url_scheme = is_secure and 'https' or 'http'
		req_method = request.method.lower()
	
		# Update server_name if a port number is required
		if (int(is_secure), server_port) not in [ (1, 443), (0, 80) ]:
			server_name = '%s:%d' % (server_name, server_port)
	
		def _coersion(result): # Ensure that values coming from the handlers have usable formats, etc
			# TODO: support other deferred types here, e.g. templates, JSON rendering, etc
			if isinstance(result, basestring):
				if isinstance(result, unicode):
					result = result.encode('utf-8')
				request.write(result)
			request.finish()	

		# Get a matching handler for this query
		match, handler = self.findroute(
				name = server_name, 
				path = fullpath, 
				scheme = url_scheme, 
				secure = is_secure,
				method = req_method,
				request = request
			)

		if handler is None:
			return resource.NoResource().render(request)

		else:
			m = getattr(handler, req_method, None)
			if callable(m):
				_deferred = defer.maybeDeferred(m, *(match.groups()), **(match.groupdict()))
				_deferred.addErrback(request.processingFailed)
				_deferred.addCallback(_coersion)

		return server.NOT_DONE_YET


def run(host = None, port = 8080, logfile = None, timeout = SERVER_TIMEOUT):
	logfile = logfile or sys.stdout
	log.startLogging(logfile)
	reactor.listenTCP(port, server.Site(PyjakResource(), timeout = timeout or 60), interface = host or '0.0.0.0')
	reactor.run()


# RequestHandler route decorator
def route(*a, **kw):
	def _method(cls):
		PyjakResource.route(cls, *a, **kw)
		return cls
	return _method


if __name__ == '__main__':
	run()
