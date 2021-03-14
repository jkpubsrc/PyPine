




import sys
import os
import typing
import grp
import pwd

import jk_typing
#import jk_prettyprintobj

from ._CommonDataObjectMixin import _CommonDataObjectMixin
from ..FileTypeInfo import FileTypeInfo





class InMemoryFile(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self,
			relFilePath:str,
			fileTypeInfo:FileTypeInfo,
			data:typing.Union[str,bytes,bytearray],
		):
		self.__relFilePath = relFilePath
		self.__fileTypeInfo = fileTypeInfo

		if isinstance(data, str):
			self.__textData = data
			self.__lengthInBytes = None
			self.__binaryData = None
		else:
			self.__textData = None
			self.__binaryData = bytes(data)
			self.__lengthInBytes = len(self.__binaryData)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def dataType(self) -> str:
		return "file"
	#

	@property
	def fileTypeInfo(self) -> FileTypeInfo:
		return self.__fileTypeInfo
	#

	@property
	def baseDirPath(self) -> str:
		return None
	#

	@property
	def relFilePath(self) -> str:
		return self.__relFilePath
	#

	@property
	def size(self) -> int:
		if self.__binaryData:
			return self.__lengthInBytes
		else:
			if self.__lengthInBytes is None:
				self.__lengthInBytes = len(self.__textData.encode("utf-8"))
			return self.__lengthInBytes
	#

	@property
	def relDirPath(self) -> str:
		return os.path.dirname(self.relFilePath)
	#

	#
	# The name of this entry
	#
	@property
	def fileName(self) -> str:
		return os.path.basename(self.relFilePath)
	#

	#
	# This is the absolute path of this entry.
	#
	@property
	def fullPath(self) -> str:
		return None
	#

	@property
	def gid(self) -> int:
		return os.getgid()
	#

	@property
	def uid(self) -> int:
		return os.getuid()
	#

	#
	# The name of the owning group
	#
	@property
	def group(self) -> typing.Union[str,None]:
		x = grp.getgrgid(self.gid)
		if x:
			return x.gr_name
		else:
			return None
	#

	#
	# The name of the owning user
	#
	@property
	def user(self) -> typing.Union[str,None]:
		x = pwd.getpwuid(self.uid)
		if x:
			return x.pw_name
		else:
			return None
	#

	@property
	def absFilePath(self) -> str:
		return None
	#

	@property
	def absDirPath(self) -> str:
		return None
	#

	@property
	def isBinary(self) -> bool:
		return bool(self.__binaryData)
	#

	@property
	def isText(self) -> bool:
		return bool(self.__textData)
	#

	@property
	def isLocal(self) -> bool:
		return True
	#

	@property
	def isLocalOnDisk(self) -> bool:
		return False
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def clone(self):
		if self.__textData is not None:
			# this file stores text data
			return InMemoryFile(self.__relFilePath, self.__fileTypeInfo, self.__textData)
		else:
			# this file stores binary data
			return InMemoryFile(self.__relFilePath, self.__fileTypeInfo, self.__binaryData)
	#

	def __str__(self):
		return "InMemoryFile<({} :: {})>".format(repr(self.relFilePath), self.fileTypeInfo)
	#

	def __repr__(self):
		return "InMemoryFile<({} :: {})>".format(repr(self.relFilePath), self.fileTypeInfo)
	#

	def getTimeStamp(self) -> float:
		return self.mtime
	#

	def getTimeStampI(self) -> int:
		return int(self.mtime)
	#

	def getFileSize(self) -> int:
		return self.size
	#

	def getMode(self) -> int:
		return 0o644
	#

	def getUID(self) -> int:
		return os.getuid()
	#

	def getGID(self) -> int:
		return os.getgid()
	#

	def readBinary(self):
		if self.__textData is None:
			return self.__binaryData
		else:
			return self.__textData.encode("utf-8")
	#

	def readText(self):
		if self.__textData is None:
			raise Exception("Not a text file!")
		else:
			return self.__textData
	#

#



