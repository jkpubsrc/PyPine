



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






class ChangeFileName(AbstractProcessor):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self,
		replaceNameWithIndex:bool = False,
		setExt:str = False,
		):

		super().__init__()

		self.__replaceNameWithIndex = replaceNameWithIndex
		self.__i = 0
		if (setExt is not None) and (setExt is not False):
			assert setExt.startswith(".")
		self.__setExt = setExt
		self.__i = None
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
		if (self.__replaceNameWithIndex is not None) and (self.__replaceNameWithIndex is not False):
			self.__i = None
		else:
			self.__i = self.__replaceNameWithIndex
	#

	def processElement(self, ctx:Context, f):
		f2 = ctx.toInMemoryFile(f)

		s = f.relDirPath
		if s:
			s += "/"

		if (self.__replaceNameWithIndex is not None) and (self.__replaceNameWithIndex is not False):
			s += str(self.__i)
			self.__i += 1
		else:
			s += f.fileNameWithoutExt

		if (self.__setExt is not None) and (self.__setExt is not False):
			s += self.__setExt
		else:
			s += f.fileExt

		return InMemoryFile(s, f2.fileTypeInfo, f2.readText())
	#

#











