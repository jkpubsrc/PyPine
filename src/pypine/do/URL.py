




import sys
import os
import typing
import datetime
import requests

import jk_furl
import jk_typing
#import jk_prettyprintobj

from ..FileTypeInfo import FileTypeInfo





_EPOCH = datetime.datetime(1970, 1, 1, 0, 0, 0, 0)




class URL(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self,
			url:str,
		):

		# normalize

		furl = jk_furl.furl(url)
		furl.path = str(furl.path).replace("//", "/")

		# ----

		self.__surl = str(furl)
		self.__furl = furl

		assert self.__furl.scheme
		assert self.__furl.host
		assert self.__furl.port

		self.__bHeadRequested = False
		self.__httpStatusCode = -1
		self.__contentLength = None
		self.__contentEncoding = None
		self.__contentMimeType = None
		self.__contentTimeStampDT = None
		self.__contentTimeStampSecs = None
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def dataType(self) -> str:
		return "url"
	#

	@property
	def exists(self) -> bool:
		if not self.__bHeadRequested:
			self.__retrieveMetaData()
		if (self.__contentMimeType is not None) and (200 <= self.__httpStatusCode < 400):
			return True
		else:
			return False
	#

	"""
	@property
	def fileTypeInfo(self) -> FileTypeInfo:
		return self.__fileTypeInfo
	#
	"""

	#
	# Provides information about the remote host and how to contact it for retrieving data.
	# Returns an identifier such as "https:i.pinimg.com:443" that provides information about from where the data is retrieved.
	#
	@property
	def remoteHostLocation(self) -> str:
		return "{}:{}:{}".format(self.__furl.scheme, self.__furl.host, self.__furl.port)
	#

	@property
	def relFilePath(self) -> str:
		ret = str(self.__furl.path)
		return ret
	#

	@property
	def relDirPath(self) -> typing.Union[str,None]:
		s = str(self.__furl.path)
		if s.startswith("/"):
			s = s[1:]
		if not s.endswith("/"):
			pos = s.rfind("/")
			s = s[:pos]
		if s:
			return s
		else:
			return None
	#

	#
	# The name of this entry
	#
	@property
	def fileName(self) -> typing.Union[str,None]:
		s = str(self.__furl.path)
		if s.startswith("/"):
			s = s[1:]
		if s.endswith("/"):
			return None
		pos = s.rfind("/")
		if pos < 0:
			if s:
				return s
			else:
				return None
		else:
			ret = s[pos+1:]
			if ret:
				return ret
			else:
				return None
	#

	"""
	n/a
	#
	# This is the absolute path of this entry.
	#
	@property
	def fullPath(self) -> str:
		return None
	#
	"""

	@property
	def relFilePath(self) -> str:
		s = str(self.__furl.path)
		if s.startswith("/"):
			s = s[1:]
		return s
	#

	@property
	def url(self) -> str:
		return self.__surl
	#

	@property
	def mimeType(self) -> str:
		return self.__contentMimeType
	#

	"""
	n/a
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
	"""

	@property
	def isLocal(self) -> bool:
		return False
	#

	@property
	def isLocalOnDisk(self) -> bool:
		return False
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __retrieveMetaData(self):
		try:
			r = requests.head(self.__surl)
			self.__httpStatusCode = r.status_code
			if r.status_code != 404:
				#print(r.headers)
				self.__contentMimeType = r.headers["content-type"]
				self.__contentLength = r.headers["content-length"] if "content-length" in r.headers else None
				self.__contentEncoding = r.headers["content-encoding"] if "content-encoding" in r.headers else None
				if "last-modified" in r.headers:
					self.__contentTimeStampDT = datetime.datetime.strptime(r.headers["last-modified"], "%a, %d %b %Y %H:%M:%S GMT")
					self.__contentTimeStampSecs = (self.__contentTimeStampDT - _EPOCH).total_seconds()
		except requests.ConnectionError as ee:
			self.__httpStatusCode = 404

		self.__bHeadRequested = True
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	"""
	def clone(self):
		if self.__textData is not None:
			# this file stores text data
			return InMemoryFile(self.__relFilePath, self.__fileTypeInfo, self.__textData)
		else:
			# this file stores binary data
			return InMemoryFile(self.__relFilePath, self.__fileTypeInfo, self.__binaryData)
	#"""

	def __str__(self):
		return "URL<({})>".format(repr(self.__surl))
	#

	def __repr__(self):
		return "URL<({})>".format(repr(self.__surl))
	#

	def getTimeStamp(self) -> typing.Union[float,None]:
		if self.__contentTimeStampDT:
			return self.__contentTimeStampSecs
		return None
	#

	def getTimeStampI(self) -> typing.Union[int,None]:
		ret = self.getTimeStamp()
		if ret is None:
			return ret
		return int(ret)
	#

	def getFileSize(self) -> typing.Union[int,None]:
		if not self.__bHeadRequested:
			self.__retrieveMetaData()

		return self.__contentLength
	#

	"""
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
	"""

#



