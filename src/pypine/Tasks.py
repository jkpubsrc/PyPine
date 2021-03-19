



import re
import os
import typing

import jk_typing
#import jk_prettyprintobj
import jk_argparsing


from ._INode import _INode
from ._Chain import _Chain
from .Context import Context
from .Task import Task





_INVALID_TASK_NAMES = [ "help" ]





class Tasks(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self):
		self.__tasks = {}
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __isValidTaskName(self, taskName:str) -> bool:
		if not isinstance(taskName, str):
			return False

		if taskName in _INVALID_TASK_NAMES:
			return False

		return re.match("^[a-zA-Z][a-zA-Z0-9_-]*$", taskName) is not None
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def ensureValidTaskNameE(self, taskName:str):
		if not self.__isValidTaskName(taskName):
			raise Exception("Not a valid task name: '{}'".format(repr(taskName)))
	#

	@jk_typing.checkFunctionSignature()
	def add(self, taskName:str, description:str, processors:typing.Union[tuple,list]) -> Task:
		self.ensureValidTaskNameE(taskName)

		chain = _Chain(*processors)
		task = Task(taskName, chain)
		self.__tasks[taskName] = description, task
		return task
	#

	@jk_typing.checkFunctionSignature()
	def run(self, taskName:str, verbosityLevel:int = 1):
		taskRecord = self.__tasks.get(taskName)
		if not taskRecord:
			raise Exception("No such task: {}".format(taskName))
		description, task = taskRecord

		ctx = Context(self, verbosityLevel, bCleanup=True)
		try:
			task.run(ctx, taskName, None)
		finally:
			try:
				ctx.cleanup()
			except Exception as ee:
				ctx.printError(None, "Cleanup failed! ({})", repr(ee))
	#		

	@jk_typing.checkFunctionSignature()
	def getE(self, taskName:str):
		taskRecord = self.__tasks.get(taskName)
		if not taskRecord:
			raise Exception("No such task: {}".format(taskName))
		description, task = taskRecord
		return task
	#		

	#
	# This is a hook method.
	# It is invoked by <c>cli()</c> with a preinitialized <c>ArgsParser</c> object to provide the possibility for further initializiing this object.
	#
	def initializeArgsParser(self, argsParser:jk_argparsing.ArgsParser):
		pass
	#

	@jk_typing.checkFunctionSignature()
	def cli(self, appPath:str, verbosityLevel:int = 1):
		ap = jk_argparsing.ArgsParser(os.path.basename(appPath), "Runs Python based tasks.")

		ap.optionDataDefaults.set("help", False)
		ap.optionDataDefaults.set("verbosityLevel1", 0)
		ap.optionDataDefaults.set("verbosityLevel2", 0)

		ap.createOption("h", "help", "Display this help text.").onOption = \
			lambda argOption, argOptionArguments, parsedArgs: \
				parsedArgs.optionData.set("help", True)
		ap.createOption(None, "verbose", "Be verbose and print some information.").onOption = \
			lambda argOption, argOptionArguments, parsedArgs: \
				parsedArgs.optionData.set("verbosityLevel1", 1)
		ap.createOption(None, "very-verbose", "Be even more verbose and print a lot of detailed information.").onOption = \
			lambda argOption, argOptionArguments, parsedArgs: \
				parsedArgs.optionData.set("verbosityLevel2", 2)

		ap.titleCommandsStd = "Standard Commands"
		ap.createCommand("help", "Displays this help text.")
		"""
		ap.createCommand("pypine-ext-ls", "List all PyPine extensions installed.")
		ap.createCommand("pypine-ext-search", "Search for PyPine extensions online.").expectString("key", minLength=1)
		"""

		ap.titleCommandsExtra = "Task Commands"

		self.initializeArgsParser(ap)

		for taskName in self.__tasks.keys():
			description, pipe = self.__tasks[taskName]
			if not ap.hasCommand(taskName):
				ap.createExtraCommand(taskName, description)

		ap.createAuthor("Jürgen Knauth", "jk@binary-overflow.de", "PyPine framework")

		# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
		#		try install bash completion file

		appPath = os.path.abspath(appPath)
		ap.installLocalBashCompletion(appPath)

		# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
		#		parse command line arguments

		parsedArgs = ap.parse()

		# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
		#		maybe: show help

		if ("help" in parsedArgs.programArgs) or parsedArgs.optionData["help"]:
			ap.showHelp()
			return

		# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

		"""
		if ("pypine-ext-ls" in parsedArgs.programArgs) or parsedArgs.optionData["pyPineExt-listInstalled"]:
			# TODO: scan /usr/local/lib/pythonX.X/dist-packages for packages
			return
		"""

		# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
		#		maybe: run default command

		if not parsedArgs.programArgs:
			defaultTask = self.__tasks.get("default")
			if defaultTask:
				self.run("default", max(verbosityLevel, parsedArgs.optionData["verbosityLevel1"], parsedArgs.optionData["verbosityLevel2"]))
				return
			ap.showHelp()
			return

		# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
		#		now: run commands specified

		for taskName in parsedArgs.programArgs:
			self.run(taskName, max(verbosityLevel, parsedArgs.optionData["verbosityLevel1"], parsedArgs.optionData["verbosityLevel2"]))
	#

#





