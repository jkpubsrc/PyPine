



import os
import typing

import jk_typing

from ..FileTypeInfo import FileTypeInfo
from ..do.DiskFile import DiskFile
from ..do.InMemoryFile import InMemoryFile
from ..Context import Context
from ..AbstractProcessor import AbstractProcessor






class SrcFromDict(AbstractProcessor):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, jData:dict):
		super().__init__()

		assert isinstance(jData, dict)

		self.__jData = jData
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
		for k in sorted(self.__jData.keys()):
			v = self.__jData[k]
			assert isinstance(v, (str, bytes, bytearray))

			yield InMemoryFile(k, FileTypeInfo.guessFromFileName(k), v)
	#

#






