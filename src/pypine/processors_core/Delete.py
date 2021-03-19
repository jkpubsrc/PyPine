



import os
import typing
import io

import jk_typing
import jk_utils

from ..ErrorMode import ErrorMode
from ..FileTypeInfo import FileTypeInfo
from ..do.DiskFile import DiskFile
from ..do.InMemoryFile import InMemoryFile
from ..Context import Context
from ..AbstractProcessor import AbstractProcessor






class Delete(AbstractProcessor):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, bDeleteEmptyDirs:bool = False, errModeDeleteFiles:ErrorMode = ErrorMode.Fail, errModeDeleteDirs:ErrorMode = ErrorMode.Fail):
		super().__init__()

		self.__errModeDeleteFiles = errModeDeleteFiles
		self.__errModeDeleteDirs = errModeDeleteDirs
		self.__bDeleteEmptyDirs = bDeleteEmptyDirs
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def processorDetailsHR(self) -> str:
		flags = [
			"errModeDeleteFiles:" + str(self.__errModeDeleteFiles),
			"errModeDeleteDirs:" + str(self.__errModeDeleteDirs),
		]
		if self.__bDeleteEmptyDirs:
			flags.append("deleteEmptyDirs")

		return ",".join(flags)
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def isProcessable(self, f) -> bool:
		return isinstance(f, DiskFile)
	#

	def initializeProcessing(self, ctx:Context):
		self.__deleteDirectories = set()
	#

	def processElement(self, ctx:Context, f):
		if not isinstance(f, DiskFile):
			ctx.printWarning(self, "Not a local disk file: " + f.relFilePath)
			return None

		if self.__errModeDeleteFiles == ErrorMode.Ignore:
			try:
				os.unlink(f.absFilePath)
			except Exception as ee:
				pass

		elif self.__errModeDeleteFiles == ErrorMode.Warn:
			try:
				os.unlink(f.absFilePath)
			except Exception as ee:
				ctx.printWarning(self, "Failed to delete file {}: " + f.relFilePath)

		elif self.__errModeDeleteFiles == ErrorMode.Fail:
			os.unlink(f.absFilePath)

		else:
			raise jk_utils.ImplementationError()

		if self.__bDeleteEmptyDirs:
			if not f.baseDirPath:
				self.__deleteDirectories.add((f.absDirPath, f.baseDirPath))
	#

	def processingCompleted(self, ctx:Context):
		if self.__deleteDirectories:
			_sortedData = reversed(sorted(self.__deleteDirectories))

			if self.__errModeDeleteDirs == ErrorMode.Ignore:
				for dirPath, baseDirPath in _sortedData:
					try:
						os.rmdir(dirPath)
					except OSError as ee:
						s = str(ee)
						if not s.startswith("[Errno 39] Directory not empty:"):
							raise

			elif self.__errModeDeleteDirs == ErrorMode.Warn:
				for dirPath, baseDirPath in _sortedData:
					try:
						os.rmdir(dirPath)
					except OSError as ee:
						s = str(ee)
						if s.startswith("[Errno 39] Directory not empty:"):
							p = dirPath[len(baseDirPath):]
							if p.startswith(os.path.sep):
								p = p[1:]
							ctx.printWarning(self, "Can't delete directory because it is not empty: " + p)
						else:
							raise

			elif self.__errModeDeleteDirs == ErrorMode.Fail:
				for dirPath, baseDirPath in _sortedData:
					os.rmdir(dirPath)

			else:
				raise jk_utils.ImplementationError()

			self.__deleteDirectories.clear()
	#

#






