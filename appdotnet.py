#!/usr/bin/env python

"""appdotnet

Usage:
  appdotnet authenticate <client_id>
  appdotnet accesstoken <access_token>
  appdotnet global [--raw]
  appdotnet
  appdotnet -h | --help
  appdotnet --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

import re
import sys

import requests # pip install --user requests
import envoy # pip install --user envoy
import docopt # pip install --user docopt
import blessings
import json
import defaults

class AppDotNet(object):
	def __init__(self):
		self.config = defaults.Defaults()

		self.config.registration = [
			('Service', 'URL', 'https://alpha-api.app.net/stream/0'),
			('Authentication', 'redirect_uri', 'x-appdotnethelper:///'),
			('Authentication', 'URL', 'https://alpha.app.net/oauth/authenticate'),
			]
    
	############################################################################

	@property
	def client_id(self):
		return self.config.get('Authentication', 'client_id')

	@client_id.setter
	def client_id(self, client_id):
		self.config.set('Authentication', 'client_id', client_id)

	@property
	def accessToken(self):
		return self.config.get('Authentication', 'access_token')

	@accessToken.setter
	def accessToken(self, accessToken):
		self.config.set('Authentication', 'access_token', accessToken)

	def synchronize(self):
		self.config.synchronize()

	############################################################################

	def authenticate(self):
		theRedirectURI = self.config.get('Authentication', 'redirect_uri')
		theScopes = 'stream email write_post follow messages export'
		
		theURL = '%(URL)s?client_id=%(client_id)s&response_type=token&redirect_uri=%(redirect_uri)s&scope=%(scopes)s'
		
		theURL = theURL % dict(
			URL = self.config.get('Authentication', 'URL'),
			client_id = self.client_id,
			redirect_uri=theRedirectURI,
			scopes=theScopes)
		
		# theURL = re.sub(r'[\n\r][ \t]*', '', theURL)
		theURL = re.sub(r' ', '%20', theURL)
		theCommand = 'open \'%s\'' % theURL
		r = envoy.run(theCommand)

	def retrieve_global_stream(self, min_id = None, max_id = None, count = None, include_user = True, include_annotations = True, include_replies = True):
		theURL = '{URL}/posts/stream/global'.format(URL = self.config.get('Service', 'URL'))
		params = {}
		if min_id:
			params['min_id'] = min_id
		if max_id:
			params['max_id'] = max_id
		if count:
			params['count'] = count
		params['include_user'] = include_user 
		params['include_annotations'] = include_annotations
		params['include_replies'] = include_replies
		
		theHeaders =  { 'Authorization': 'Bearer %s' % self.accessToken }
		r = requests.get(theURL, headers = theHeaders, params = params)
		return r

	def list_global(self, raw = False):
		r = self.retrieve_global_stream()
		t = blessings.Terminal()
		if raw:
			print json.dumps(r.json, indent = 4)
		else:
			for thePost in r.json:
				d = {
					'user': thePost['user']['username'],
					'text': thePost['text'],
					}
				print u'{t.standout}{user}{t.normal}: {text}'.format(t = t, **d)
		
################################################################################

if __name__ == '__main__':
	argv = sys.argv[1:]
	arguments = docopt.docopt(__doc__, argv=argv, version='appdotnet')
	print arguments
	
	theApp = AppDotNet()
	
	if arguments['authenticate'] and arguments['<client_id>']:
		theApp.client_id = arguments['<client_id>']
		theApp.synchronize()
		theApp.authenticate()
	elif arguments['accesstoken'] and arguments['<access_token>']:
		theApp.accessToken = arguments['<access_token>']
		theApp.synchronize()
	elif arguments['global']:
		theApp.list_global(raw = arguments['--raw'])
