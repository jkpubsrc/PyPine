






import datetime
import os
import typing
import tempfile
import shutil

import jk_typing
#import jk_prettyprintobj

from .do.DiskFile import DiskFile
from .do.InMemoryFile import InMemoryFile





_RESET = "\033[0m"
_BLACK = "\033[0;30m"
_RED = "\033[0;31m"
_GREEN = "\033[0;32m"
_YELLOW = "\033[1;33m"
_BLUE = "\033[1;34m"
_MAGENTA = "\033[1;35m"
_CYAN = "\033[1;36m"
_WHITE = "\033[1;37m"

_DARK_BLACK = "\033[38:5:0m"
_DARK_RED = "\033[38:5:1m"
_DARK_GREEN = "\033[38:5:2m"
_DARK_YELLOW = "\033[38:5:3m"
_DARK_BLUE = "\033[38:5:4m"
_DARK_MAGENTA = "\033[38:5:5m"
_DARK_CYAN = "\033[38:5:6m"
_DARK_WHITE = "\033[38:5:7m"

_LIGHT_BLACK = "\033[1;90m"
_LIGHT_RED = "\033[1;91m"
_LIGHT_GREEN = "\033[1;92m"
_LIGHT_YELLOW = "\033[1;93m"
_LIGHT_BLUE = "\033[1;94m"
_LIGHT_MAGENTA = "\033[1;95m"
_LIGHT_CYAN = "\033[1;96m"
_LIGHT_WHITE = "\033[1;97m"





class Context(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, tasks, verbosityLevel:int = 1, bCleanup:bool = True):
		self.t0 = datetime.datetime.now()

		self.__tasks = tasks
		self.verbosityLevel = verbosityLevel
		self.bCleanup = bCleanup

		self.__mainTempDir = None
		self.__allTempDirs = []

		self.__localFileDir = None
		self.__localFileNames = set()

		self.__indent = ""

		self.__localData = {}

		self.__directoriesExist = set()
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def localData(self) -> dict:
		return self.__localData
	#

	@property
	def tasks(self):
		return self.__tasks
	#

	@property
	def durationSeconds(self) -> float:
		return (datetime.datetime.now() - self.t0).total_seconds()
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def printVerbose(self, caller, message:str, *args, **kwargs):
		sCaller = (" " + getattr(caller, "processorTypeName", "")) if caller is not None else ""
		if self.verbosityLevel > 0:
			dt = datetime.datetime.now()
			sPrefix = "{}{}[{:02d}:{:02d}:{:02d}]{}{}{}{}".format(self.__indent, _DARK_CYAN, dt.hour, dt.minute, dt.second, _RESET, _LIGHT_BLACK, sCaller, _RESET)
		if args or kwargs:
			print(sPrefix, message.format(*args, **kwargs))
		else:
			print(sPrefix, message)
	#

	def printDetail(self, caller, message:str, *args, **kwargs):
		sCaller = (" " + getattr(caller, "processorTypeName", "")) if caller is not None else ""
		dt = datetime.datetime.now()
		sPrefix = "{}{}[{:02d}:{:02d}:{:02d}]{}{}{}{}".format(self.__indent, _DARK_CYAN, dt.hour, dt.minute, dt.second, _RESET, _LIGHT_BLACK, sCaller, _RESET)
		if args or kwargs:
			print(sPrefix, message.format(*args, **kwargs))
		else:
			print(sPrefix, message)
	#

	def printTaskBegin(self, message:str, *args, **kwargs):
		dt = datetime.datetime.now()
		sPrefix = "{}{}[{:02d}:{:02d}:{:02d}]{}".format(self.__indent, _DARK_CYAN, dt.hour, dt.minute, dt.second, _RESET)
		print(sPrefix, _LIGHT_CYAN + message.format(*args, **kwargs) + _RESET)
		self.__indent += "    "
	#

	def printTaskSucceeded(self, message:str, *args, **kwargs):
		if self.__indent:
			self.__indent = self.__indent[:-4]
		else:
			raise Exception("No prior call to printTaskBegin()!")
		dt = datetime.datetime.now()
		sPrefix = "{}{}[{:02d}:{:02d}:{:02d}]{}".format(self.__indent, _DARK_CYAN, dt.hour, dt.minute, dt.second, _RESET)
		print(sPrefix, _GREEN + message.format(*args, **kwargs) + _RESET)
	#

	def printError(self, caller, message:str, *args, **kwargs):
		sCaller = (" " + getattr(caller, "processorTypeName", "")) if caller is not None else ""
		dt = datetime.datetime.now()
		sPrefix = "{}{}[{:02d}:{:02d}:{:02d}]{}{}{}{}".format(self.__indent, _DARK_CYAN, dt.hour, dt.minute, dt.second, _RESET, _LIGHT_BLACK, sCaller, _RESET)
		print(sPrefix, _RED + "ERR: " + message.format(*args, **kwargs) + _RESET)
	#

	def printWarning(self, caller, message:str, *args, **kwargs):
		sCaller = (" " + getattr(caller, "processorTypeName", "")) if caller is not None else ""
		dt = datetime.datetime.now()
		sPrefix = "{}{}[{:02d}:{:02d}:{:02d}]{}{}{}{}".format(self.__indent, _DARK_CYAN, dt.hour, dt.minute, dt.second, _RESET, _LIGHT_BLACK, sCaller, _RESET)
		print(sPrefix, _YELLOW + "WARN: " + message.format(*args, **kwargs) + _RESET)
	#

	################################################################################################################################

	def toInMemoryFile(self, dataObj, cloneInMemoryFiles:bool=False) -> InMemoryFile:
		if isinstance(dataObj, InMemoryFile):
			if cloneInMemoryFiles:
				return dataObj.clone()
			else:
				return dataObj

		assert dataObj.fileName
		assert dataObj.relFilePath

		if dataObj.isText:
			rawData = dataObj.readText()
		else:
			rawData = dataObj.readBinary()

		f2 = InMemoryFile(dataObj.relFilePath, dataObj.fileTypeInfo, rawData)
		return f2
	#

	def toLocalDiskFile(self, dataObj) -> DiskFile:
		if isinstance(dataObj, DiskFile):
			return dataObj

		assert dataObj.fileName

		# create temp dir if we haven"t one yet
		if self.__localFileDir is None:
			self.__localFileDir = self.newTempDir()
		else:
			if dataObj.fileName in self.__localFileNames:
				# just create a new temp directory
				self.__localFileDir = self.newTempDir()
				self.__localFileNames = set()

		# save file
		destFilePath = os.path.join(self.__localFileDir, dataObj.fileName)
		with open(destFilePath, "wb") as f:
			f.write(dataObj.readBinary())

		# return new local file
		f = DiskFile.fromFile(self.__localFileDir, destFilePath)
		return f
	#

	def newTempFile(self) -> str:
		if self.__mainTempDir is None:
			self.__mainTempDir = tempfile.mkdtemp(prefix="pypine-")
			self.__allTempDirs.append(self.__mainTempDir)
		return tempfile.mktemp(dir=self.__mainTempDir)
	#

	def newTempDir(self) -> str:
		tempDirPath = tempfile.mkdtemp(prefix="pypine-")
		self.__allTempDirs.append(tempDirPath)
		return tempDirPath
	#

	def ensureDirExists(self, absDirPath:str):
		if absDirPath in self.__directoriesExist:
			return
		os.makedirs(absDirPath, exist_ok=True)
		self.__directoriesExist.add(absDirPath)
	#

	def cleanup(self):
		if self.bCleanup:
			for tempDir in self.__allTempDirs:
				shutil.rmtree(tempDir)
			self.__allTempDirs.clear()
		else:
			for tempDir in self.__allTempDirs:
				self.printWarning(None, "Skipping cleanup:", tempDir)
			self.__allTempDirs.clear()

		self.__directoriesExist.clear()
	#

#















