#!/usr/bin/env python

import re
import sys
import ConfigParser
import os
import atexit

class Defaults(object):

	def __init__(self):
		self.registration = []
		atexit.register(self.synchronize)
	
	@property
	def name(self):
		if not hasattr(self, '_name'):
			self._name = os.path.splitext(os.path.split(sys.argv[0])[1])[0]
		return self._name

	@property
	def path(self):
		if not hasattr(self, '_path'):
			self._path = os.path.expanduser(os.path.join('~/', '.' + self.name + '.cfg'))
		return self._path

	@property
	def adaptors(self):
		if not hasattr(self, '_adaptors'):
			self._adaptors = [
				ConfigParserAdaptor(ConfigParser.ConfigParser(), self.path),
				ListAdaptor(self.registration),
				]
		return self._adaptors

	def get(self, section, key):
		value = None
		for adaptor in self.adaptors:
			value = adaptor.get(section, key)
			if value:
				break
		return value

	def set(self, section, key, value):
		adaptor = self.adaptors[0]
		adaptor.set(section, key, value)

	def synchronize(self):
		for adaptor in self.adaptors:
			adaptor.synchronize()

################################################################################

class ListAdaptor(object):
	def __init__(self, target):
		self.target = target
	
	def get(self, section, key):
		s, k, v = [(s, k, v) for s, k, v in self.target if s == section and k == key][0]
		return v

	def synchronize(self):
		pass

################################################################################

class ConfigParserAdaptor(object):
	def __init__(self, config, path):
		self.config = config
		self.path = path
		self.config.read(self.path)

	def get(self, section, key):
		value = None
		if self.config.has_option(section, key):
			value = self.config.get(section, key)
		return value

	def set(self, section, key, value):
		if not self.config.has_section(section):
			self.config.add_section(section)
		self.config.set(section, key, value)

	def synchronize(self):
		self.config.write(file(self.path, 'wb'))

################################################################################

if __name__ == '__main__':
	defaults = Defaults()
	defaults.set('section', 'key', 'value')
	print defaults.get('section', 'key')
