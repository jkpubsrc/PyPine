



import os
import typing
import re

import jk_typing

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
	@jk_typing.checkFunctionSignature()
	def __init__(self,
			removeEnumerationPrefix:bool = False,
			replaceNameWithIndex:typing.Union[bool,int] = False,
			setExt:typing.Union[bool,str] = False,
		):

		super().__init__()

		# ----

		self.__removeEnumerationPrefix = None
		if (removeEnumerationPrefix is not None) and (removeEnumerationPrefix is not False):
			assert isinstance(removeEnumerationPrefix, bool)
			if removeEnumerationPrefix:
				self.__removeEnumerationPrefix = True

		# ----

		self.__replaceNameWithIndex = None
		if (replaceNameWithIndex is not None) and (replaceNameWithIndex is not False):
			if isinstance(replaceNameWithIndex, bool):
				if replaceNameWithIndex:
					self.__replaceNameWithIndex = 0
				else:
					self.__replaceNameWithIndex = None
			elif isinstance(replaceNameWithIndex, int):
				assert replaceNameWithIndex >= 0
				self.__replaceNameWithIndex = replaceNameWithIndex
			else:
				raise TypeError("replaceNameWithIndex")
		self.__replaceNameWithIndexI = None

		# ----

		if (setExt is not None) and (setExt is not False):
			assert isinstance(setExt, str)
			assert setExt.startswith(".")
		self.__setExt = setExt
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
		if self.__replaceNameWithIndex is not None:
			self.__replaceNameWithIndexI = self.__replaceNameWithIndex
	#

	def processElement(self, ctx:Context, f):
		f2 = ctx.toInMemoryFile(f)
		_relDirPath = f.relDirPath
		if _relDirPath:
			_relDirPath += "/"

		_fileNameWithoutExt = f.fileNameWithoutExt
		_fileExt = f.fileExt

		# ----

		if self.__removeEnumerationPrefix is not None:
			m = re.match("^([0-9]+\s*)(-\s*)?(?P<fn>.*)$", _fileNameWithoutExt)
			if m:
				_fileNameWithoutExt = m.group("fn")
				assert _fileNameWithoutExt

		# ----

		if self.__replaceNameWithIndex is not None:
			_fileNameWithoutExt = str(self.__replaceNameWithIndexI)
			self.__replaceNameWithIndexI += 1

		# ----

		if self.__setExt is not None:
			_fileExt = self.__setExt
		
		# ----

		return InMemoryFile(_relDirPath + _fileNameWithoutExt + _fileExt, f2.fileTypeInfo, f2.readText())
	#

#











