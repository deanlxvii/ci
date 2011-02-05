import sys, os

class Application(object):
	name = '.ci'

	def __init__(self):
		self.dir = dict()
		if sys.platform == 'linux2':
			self.linux_config()

	def linux_config(self):
		self.dir['home'] = self.set_home()

	def win_config(self):
		pass


	def set_home(self):
		home = os.path.join(os.environ['HOME'], Application.name)
		self.check_and_create(home)
		return home

	def check_and_create(self, path):
		if not os.path.isdir(path):
			os.mkdir(path)
