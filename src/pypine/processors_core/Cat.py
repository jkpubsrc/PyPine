



import os
import typing

import jk_typing
import jk_utils
import jk_logging
import jk_json
import jk_prettyprintobj


from ..FileTypeInfo import FileTypeInfo
from ..do.DiskFile import DiskFile
from ..do.InMemoryFile import InMemoryFile
from ..Context import Context
from ..AbstractProcessor import AbstractProcessor






class Cat(AbstractProcessor):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, **kwargs):
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
		ctx.printDetail(self, "=" * 120)
		ctx.printDetail(self, f.__class__.__name__ + ": " + f.relFilePath)
		ctx.printDetail(self, "Size: " + str(f.getFileSize()))
		ctx.printDetail(self, "isBinary: " + str(f.isBinary))
		ctx.printDetail(self, "isText: " + str(f.isText))
		ctx.printDetail(self, "-" * 120)
		if f.isText:
			text = f.readText()
			for s in text.split("\n"):
				ctx.printDetail(self, s)
		else:
			ctx.printDetail(self, "(binary file)")
		ctx.printDetail(self, "=" * 120)
		return f
	#

#






