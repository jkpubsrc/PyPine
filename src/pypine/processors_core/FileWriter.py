



import os
import typing

import jk_typing

from ..do.DiskFile import DiskFile
from ..Context import Context
from ..AbstractProcessor import AbstractProcessor
from ..EnumAction import EnumAction







#
# This component stores files.
#
class FileWriter(AbstractProcessor):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, outputDirPath:str):
		super().__init__()

		self.__outputDirPath = os.path.normpath(os.path.abspath(outputDirPath))
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def processorDetailsHR(self) -> str:
		return self.__outputDirPath
	#

	@property
	def processorTypeName(self) -> str:
		return "dest"
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def initializeProcessing(self, ctx:Context):
		# TODO: clean the target directory by recursively removing all files and directories.
		pass
	#

	def processableDataTypes(self) -> list:
		return [ "file" ]
	#

	def actionIfUnprocessable(self) -> EnumAction:
		return EnumAction.Warn
	#

	def processElement(self, ctx:Context, f):
		# TODO: set file modification time and mode on write?

		absDirPath = os.path.join(self.__outputDirPath, f.relDirPath)

		os.makedirs(absDirPath, exist_ok=True)

		ctx.printDetail(self, "Writing: " + f.relFilePath)
		absFilePath = os.path.join(absDirPath, f.fileName)
		with open(absFilePath, "wb") as fout:
			fout.write(f.readBinary())

		f2 = DiskFile.fromFile(self.__outputDirPath, absFilePath)
		return f2
	#

#






