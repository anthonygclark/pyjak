#!/usr/bin/python

from http import server as server
import service


# Routes will be matched in order.
# Only the first matching route will be served.
# Routes are matched based on URL pattern and 
# method of the HTTP request (i.e. HTTP GET
# is mapped to the 'get' method of RequestHandler


@server.route(r'^/test$')
class TestHandler(server.RequestHandler):
	def get(self, *a, **kw):
		return 'this was a test!\n\n'


@server.route(r'^/test/2$')
class AnotherHandler(server.RequestHandler):
	def get(self, *a, **kw):
		return 'this is a different test.\n\n'

# This one never runs, since it's handled by the prior two
@server.route(r'^/test(/2)?$')
class CommonHandler(server.RequestHandler):
	def get(self, tailval):
		return '# Tail value was: %r\n\n' % (tailval)

# matches 3 (not matched by any other)
@server.route(r'^/test/3$')
class TestHandler(server.RequestHandler):
	def get(self, *a, **kw):
		return 'this was the #3 test!\n\n'


if __name__ == '__main__':
	service.run()
