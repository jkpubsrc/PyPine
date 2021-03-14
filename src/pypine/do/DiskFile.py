




import os
import stat
import typing

import jk_typing
#import jk_prettyprintobj
import jk_pathpatternmatcher2

from ._CommonDataObjectMixin import _CommonDataObjectMixin
from ..FileTypeInfo import FileTypeInfo





class DiskFile(jk_pathpatternmatcher2.Entry, _CommonDataObjectMixin):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self,
			absBaseDirPath:str,
			relFilePath:str,
			typeID:str,
			mtime:float,
			uid:int,
			gid:int,
			size:int,
			mode:int,
			exception:Exception,
			fileTypeInfo:FileTypeInfo = None,
		):
		super().__init__(absBaseDirPath, relFilePath, typeID, mtime, uid, gid, size, mode, exception)
		self.fileTypeInfo = fileTypeInfo
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def dataType(self) -> str:
		return "file"
	#

	"""
	@property
	def relFilePath(self) -> str:
		return self.relPath
	#

	@property
	def baseDirPath(self) -> str:
		return self.relPath
	#
	"""

	@property
	def absFilePath(self) -> str:
		return self.fullPath
	#

	@property
	def absDirPath(self) -> str:
		return self.dirPath
	#

	@property
	def isBinary(self) -> bool:
		if (self.fileTypeInfo is None) or (self.fileTypeInfo.fileDataType == "b"):
			return True
		else:
			return False
	#

	@property
	def isText(self) -> bool:
		if (self.fileTypeInfo is None) or (self.fileTypeInfo.fileDataType == "b"):
			return False
		else:
			return True
	#

	@property
	def isLocal(self) -> bool:
		return True
	#

	@property
	def isLocalOnDisk(self) -> bool:
		return True
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def clone(self):
		return DiskFile(self.baseDirPath, self.relFilePath, self.typeID, self.mtime, self.uid, self.gid, self.size, self.mode, self.exception, self.fileTypeInfo)
	#

	def __str__(self):
		return "DiskFile<({} :: {})>".format(repr(self.relFilePath), self.fileTypeInfo)
	#

	def __repr__(self):
		return "DiskFile<({} :: {})>".format(repr(self.relFilePath), self.fileTypeInfo)
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
		return self.mode
	#

	def getUID(self) -> int:
		return self.uid
	#

	def getGID(self) -> int:
		return self.gid
	#

	def readBinary(self):
		"""
		if (self.fileTypeInfo is None) or (self.fileTypeInfo.fileDataType == "b"):
			with open(self.absFilePath, "rb") as f:
				return f.read()
		else:
			with open(self.absFilePath, "r") as f:
				return f.read().encode("utf-8")
		"""

		# let's assume that if this is a text file it already is using an encoding of UTF-8.
		with open(self.absFilePath, "rb") as f:
			return f.read()
	#

	def readText(self):
		if not self.isText:
			raise Exception("Not a text file!")
		else:
			with open(self.absFilePath, "r") as f:
				return f.read()
	#

	################################################################################################################################
	## Public Static Methods
	################################################################################################################################

	@staticmethod
	def fromFile(absBaseDirPath:str, absFilePath:str, fileTypeInfo:FileTypeInfo = None):
		assert os.path.isabs(absBaseDirPath)
		assert os.path.isabs(absFilePath)
		assert absFilePath.startswith(absBaseDirPath)

		statResult = os.lstat(absFilePath)
		assert stat.S_ISREG(statResult.st_mode)

		relFilePath = os.path.relpath(absFilePath, absBaseDirPath)

		if fileTypeInfo is None:
			fileTypeInfo = FileTypeInfo.guessFromFileName(relFilePath)

		return DiskFile(
			absBaseDirPath,
			relFilePath,
			"f",
			statResult.st_mtime,
			statResult.st_uid,
			statResult.st_gid,
			statResult.st_size,
			statResult.st_mode,
			exception=None,
			fileTypeInfo=fileTypeInfo)
	#

#



