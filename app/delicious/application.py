import sys, os, os.path
from ci.app import Application as BaseApplication

class Application(BaseApplication):
	name = 'delicious'

	def __init__(self):
		BaseApplication.__init__(self)

	def linux_config(self):
		BaseApplication.set_home(self)
		home = os.path.join(os.environ['HOME'], os.path.join(BaseApplication.name,Application.name))
		self.dir['home'] = self.set_dir(home)
		self.dir['data'] = self.set_dir(os.path.join(self.dir['home'],'dat'))
		self.dir['log'] = self.set_dir(os.path.join(self.dir['home'],'log'))

	def set_dir(self, dir):
		self.check_and_create(dir)
		return dir

