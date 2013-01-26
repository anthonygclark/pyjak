#!/usr/bin/python

import json as _json
from xml.parsers import expat as _xml

# As per http://jcalderone.livejournal.com/55680.html,
# Consider using JSONEncoder.iterencode for non-blocking output
# For prototyping purproses, focus on JSON before supporting XML

# TODO: based on Content-Type header, parse as XML or JSON; return data object
def request_data(request):
	pass

# TODO: based on Accept header, render data object as XML or JSON; return string
def response_data(request, data):
	pass
