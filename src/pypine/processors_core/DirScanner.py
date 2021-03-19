




import os
import typing

import jk_typing
import jk_pathpatternmatcher2

from ..FileTypeInfo import FileTypeInfo
from ..do.DiskFile import DiskFile
from ..Context import Context
from ..AbstractProcessor import AbstractProcessor







class DirScanner(AbstractProcessor):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, baseDirPath:str, *filePatterns, fileTypeInfo:FileTypeInfo = None):
		super().__init__()

		self.__processorDetailsHR = baseDirPath + ":" + ",".join(filePatterns)

		assert filePatterns
		for filePattern in filePatterns:
			assert isinstance(filePattern, str)
			assert not filePattern.startswith("/")
			assert not filePattern.startswith("\\")
			assert not filePattern.startswith(".")

		self.__baseDirPath = os.path.normpath(os.path.abspath(baseDirPath))
		self.__filePatterns = filePatterns
		self.__fileTypeInfo = fileTypeInfo

		self.__dirWalker = None
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def processorTypeName(self) -> str:
		return "src"
	#

	@property
	def processorDetailsHR(self) -> str:
		return self.__processorDetailsHR
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def isProcessable(self, f) -> bool:
		return True
	#

	def initializeProcessing(self, ctx:Context):
		self.__dirWalker = jk_pathpatternmatcher2.walk(
			self.__baseDirPath,
			emitBaseDirs=False,
			emitDirs=False,
			emitErrorEntries=False,
			emitLinks=False,
			clazz=DiskFile,
			acceptFilePathPatterns=self.__filePatterns,
			sort=True,
		)
	#

	def processElement(self, ctx:Context, f):
		if f is not None:
			yield f

		for f in self.__dirWalker:
			if self.__fileTypeInfo is None:
				f.fileTypeInfo = FileTypeInfo.guessFromFileName(f.fileName)
			else:
				f.fileTypeInfo = self.__fileTypeInfo

			ctx.printVerbose(self, "Processing: {}", f.relFilePath)

			yield f
	#

#



