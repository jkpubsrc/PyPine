






import datetime
import os
import typing
import tempfile
import shutil

import jk_typing
#import jk_prettyprintobj

from .utils.Color import Color
from .do.DiskFile import DiskFile
from .do.InMemoryFile import InMemoryFile







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
			sPrefix = "{}{}[{:02d}:{:02d}:{:02d}]{}{}{}{}".format(self.__indent, Color.DARK_CYAN, dt.hour, dt.minute, dt.second, Color.RESET, Color.LIGHT_BLACK, sCaller, Color.RESET)
		if args or kwargs:
			print(sPrefix, message.format(*args, **kwargs))
		else:
			print(sPrefix, message)
	#

	def printDetail(self, caller, message:str, *args, **kwargs):
		sCaller = (" " + getattr(caller, "processorTypeName", "")) if caller is not None else ""
		dt = datetime.datetime.now()
		sPrefix = "{}{}[{:02d}:{:02d}:{:02d}]{}{}{}{}".format(self.__indent, Color.DARK_CYAN, dt.hour, dt.minute, dt.second, Color.RESET, Color.LIGHT_BLACK, sCaller, Color.RESET)
		if args or kwargs:
			print(sPrefix, message.format(*args, **kwargs))
		else:
			print(sPrefix, message)
	#

	def printTaskBegin(self, message:str, *args, **kwargs):
		dt = datetime.datetime.now()
		sPrefix = "{}{}[{:02d}:{:02d}:{:02d}]{}".format(self.__indent, Color.DARK_CYAN, dt.hour, dt.minute, dt.second, Color.RESET)
		print(sPrefix, Color.LIGHT_CYAN + message.format(*args, **kwargs) + Color.RESET)
		self.__indent += "    "
	#

	def printTaskSucceeded(self, message:str, *args, **kwargs):
		if self.__indent:
			self.__indent = self.__indent[:-4]
		else:
			raise Exception("No prior call to printTaskBegin()!")
		dt = datetime.datetime.now()
		sPrefix = "{}{}[{:02d}:{:02d}:{:02d}]{}".format(self.__indent, Color.DARK_CYAN, dt.hour, dt.minute, dt.second, Color.RESET)
		print(sPrefix, Color.GREEN + message.format(*args, **kwargs) + Color.RESET)
	#

	def printError(self, caller, message:str, *args, **kwargs):
		sCaller = (" " + getattr(caller, "processorTypeName", "")) if caller is not None else ""
		dt = datetime.datetime.now()
		sPrefix = "{}{}[{:02d}:{:02d}:{:02d}]{}{}{}{}".format(self.__indent, Color.DARK_CYAN, dt.hour, dt.minute, dt.second, Color.RESET, Color.LIGHT_BLACK, sCaller, Color.RESET)
		print(sPrefix, Color.RED + "ERR: " + message.format(*args, **kwargs) + Color.RESET)
	#

	def printWarning(self, caller, message:str, *args, **kwargs):
		sCaller = (" " + getattr(caller, "processorTypeName", "")) if caller is not None else ""
		dt = datetime.datetime.now()
		sPrefix = "{}{}[{:02d}:{:02d}:{:02d}]{}{}{}{}".format(self.__indent, Color.DARK_CYAN, dt.hour, dt.minute, dt.second, Color.RESET, Color.LIGHT_BLACK, sCaller, Color.RESET)
		print(sPrefix, Color.YELLOW + "WARN: " + message.format(*args, **kwargs) + Color.RESET)
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















