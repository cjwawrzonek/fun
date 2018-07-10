import sys


class Directory(object):
	def __init__(self, name, parent):
		self.name = name
		self.parent = parent
		self.directories = []


class Console(object):
	def __init__(self):
		self.root = Directory('/', None)
		self.cur_directory = self.root
		self.run = True

		self.commands = {
			'cd': self.cd,
			'pwd': self.pwd,
			'mkdir': self.mkdir,
			'rm': self.rm,
			'ls': self.ls,
			'quit': self.quit,
			'q': self.quit
		}

	# ------------------------------------
	# API
	# ------------------------------------

	def start(self):
		while self.run:
			inpt = raw_input('> ')
			inpt = inpt.split()
			if not inpt:
				continue
			command = inpt[0]
			if command not in self.commands.keys():
				print 'ERROR: Command [ {} ] not recognized'.format(inpt[0])
				continue
			self.commands.get(command)(inpt)

	# ------------------------------------
	# Commands
	# ------------------------------------

	def pwd(self, _):
		"""Print current directory path."""
		dir_names = []
		directory = self.cur_directory
		while directory != self.root:
			dir_names.append(directory.name)
			directory = directory.parent
		dir_names = dir_names[::-1]
		dir_string = '/'
		for name in dir_names:
			dir_string = dir_string + name + '/'
		print dir_string

	def mkdir(self, inpt):
		"""Make a new directory for each input after the command."""
		if len(inpt) < 2:
			print 'ERROR: mkdir requires a directory name as an argument.'
			return
		for name in inpt[1:]:
			new_dir = Directory(name, self.cur_directory)
			self.cur_directory.directories.append(new_dir)

	def rm(self, inpt):
		"""Remove a directory matching the name of each inpt after the command."""
		if len(inpt) < 2:
			print 'ERROR: rm requires a directory name as an argument.'
			return
		dirr = None
		for name in inpt[1:]:
			for d in self.cur_directory.directories:
				if name == d.name:
					dirr = d
					break
			if not dirr:
				print 'ERROR: No directory named {}'.format(name)
				return
			self.cur_directory.directories.remove(dirr)

	def ls(self, _):
		"""Print all sub directories in the current directory."""
		for d in self.cur_directory.directories:
			print d.name

	def cd(self, inpt):
		"""Change the current directory."""
		if len(inpt) > 2:
			print 'ERROR, USAGE: cd path/to/new/directory'
			return
		elif len(inpt) < 2:
			self.cur_directory = self.root
			return
		start_dir = self.cur_directory
		dir_string = inpt[1]
		if dir_string.endswith('/'):
			dir_string = dir_string[:-1]
		if dir_string.startswith('/'):
			dir_string = dir_string[1:]
			self.cur_directory = self.root
		dir_names = dir_string.split('/')
		for name in dir_names:
			cur_dir = self.cur_directory
			if name == '.':
				continue
			elif name == '..':
				self.cur_directory = self.cur_directory.parent
				continue
			d = self.cur_directory
			for d in self.cur_directory.directories:
				if name == d.name:
					self.cur_directory = d
					break
			if cur_dir == self.cur_directory:
				print 'ERROR: could not find [ {} ] in [ {} ]'.format(name, d.name)
				self.cur_directory = start_dir

	def quit(self, _):
		"""End the console session."""
		self.run = False


if __name__ == '__main__':
	if len(sys.argv) != 1:
		print "Usage: python console.py"
		exit()
	out = open(sys.argv[0])
	console = Console()
	console.start()
