



import os
import typing

import jk_typing

from ..FileTypeInfo import FileTypeInfo
from ..do.DiskFile import DiskFile
from ..do.InMemoryFile import InMemoryFile
from ..Context import Context
from ..AbstractProcessor import AbstractProcessor






class RunTask(AbstractProcessor):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, taskName:str):
		super().__init__()

		self.__taskName = taskName
		self.__task = None
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def initializeProcessing(self, ctx:Context):
		self.__task = ctx.tasks.getE(self.__taskName)
	#

	def processElement(self, ctx:Context, f):
		return self.__task.run(ctx, self.__taskName, f)
	#

#






