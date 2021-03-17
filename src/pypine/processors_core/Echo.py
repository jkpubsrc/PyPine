



import os
import typing
import io

#import jk_typing

from ..FileTypeInfo import FileTypeInfo
from ..do.DiskFile import DiskFile
from ..do.InMemoryFile import InMemoryFile
from ..Context import Context
from ..AbstractProcessor import AbstractProcessor






class Echo(AbstractProcessor):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self):
		super().__init__()
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

	def processElement(self, ctx:Context, f):
		ctx.printVerbose(self, str(f))
		return f
	#

#






