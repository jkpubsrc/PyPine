



import os
import typing
import re

import jk_typing
#import jk_json
#import jk_prettyprintobj











class FileTypeInfo(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	# @param	str fileDataType		General file data type: "t" for text, "b" for binary
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, textOrBinary:str, fileTypeID:str):
		assert textOrBinary in ["t", "b"]
		assert fileTypeID

		self.__fileDataType = textOrBinary
		self.__fileTypeID = fileTypeID
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	#
	# @return	str fileDataType		General file data type: "t" for text, "b" for binary
	#
	@property
	def fileDataType(self) -> str:
		return self.__fileDataType
	#

	@property
	def fileTypeID(self) -> str:
		return self.__fileTypeID
	#

	@property
	def isBinary(self) -> bool:
		return self.__fileDataType != "t"
	#

	@property
	def isText(self) -> bool:
		return self.__fileDataType == "t"
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def __str__(self):
		return "FileTypeInfo<(fileDataType='{}', fileTypeID='{}')>".format(self.__fileDataType, self.__fileTypeID)
	#

#





_FILE_TYPE_INFO_GENERIC_BINARY = FileTypeInfo("b", "generic-binary")

_FILE_TYPE_INFOS = {
	".py": FileTypeInfo("t", "python-src"),
	".java": FileTypeInfo("t", "java-src"),
	".class": FileTypeInfo("t", "java-class"),
	".jar": FileTypeInfo("b", "java-jar"),

	".py": FileTypeInfo("t", "py-src"),
	".pyc": FileTypeInfo("b", "py-bin"),

	".sh": FileTypeInfo("t", "unix-shellscript"),

	".bat": FileTypeInfo("t", "bat-shellscript"),

	".c": FileTypeInfo("t", "c-src"),
	".cpp": FileTypeInfo("t", "cpp-src"),
	".h": FileTypeInfo("t", "c-header"),

	".cs": FileTypeInfo("t", "csharp-src"),

	".pas": FileTypeInfo("t", "pascal-src"),

	".lua": FileTypeInfo("t", "lua-src"),

	".pov": FileTypeInfo("t", "povray-src"),

	".ini": FileTypeInfo("t", "inifile"),

	".html": FileTypeInfo("t", "html"),
	".htm": FileTypeInfo("t", "html"),
	".jinja": FileTypeInfo("t", "html-jinja"),
	".jinja2": FileTypeInfo("t", "html-jinja2"),
	".njk": FileTypeInfo("t", "html-nunjucks"),

	".md": FileTypeInfo("t", "markdown"),
	".mw": FileTypeInfo("t", "mediawiki"),

	".asciinema": FileTypeInfo("t", "asciinema-recording"),

	".txt": FileTypeInfo("t", "plaintext"),

	".csv": FileTypeInfo("t", "csv"),
	".tsv": FileTypeInfo("t", "tsv"),

	".css": FileTypeInfo("t", "css"),
	".less": FileTypeInfo("t", "css-less"),
	".scss": FileTypeInfo("t", "css-sass"),
	".sass": FileTypeInfo("t", "css-sass"),

	".gz": FileTypeInfo("b", "gzip"),
	".bz2": FileTypeInfo("b", "bzip"),
	".xz": FileTypeInfo("b", "xz"),
	".zip": FileTypeInfo("b", "zip"),
	".arj": FileTypeInfo("b", "arj"),
	".rar": FileTypeInfo("b", "rar"),

	".tar": FileTypeInfo("b", "tar"),
	".tar.gz": FileTypeInfo("b", "tar-gz"),
	".tgz": FileTypeInfo("b", "tar-gz"),
	".tar.bz2": FileTypeInfo("b", "tar-bz2"),
	".tar.xz": FileTypeInfo("b", "tar-xz"),

	".ps": FileTypeInfo("b", "postscript"),

	".pdf": FileTypeInfo("b", "pdf"),

	".svg": FileTypeInfo("t", "image-svg"),
	".bmp": FileTypeInfo("b", "image-bmp"),
	".tif": FileTypeInfo("b", "image-tiff"),
	".tiff": FileTypeInfo("b", "image-tiff"),
	".png": FileTypeInfo("b", "image-png"),
	".jpg": FileTypeInfo("b", "image-jpg"),
	".jpeg": FileTypeInfo("b", "image-jpg"),
	".gif": FileTypeInfo("b", "image-gif"),
	".webp": FileTypeInfo("b", "image-webp"),
}






def _guessFromFileName(fileName:str):
	fileName = os.path.basename(fileName).lower()

	m = re.match(".+(\.[a-z]+\.[a-z]+)$", fileName)
	if m:
		ext = m.groups(1)
		ret = _FILE_TYPE_INFOS.get(ext)
		if ret is not None:
			return ret

	_, ext = os.path.splitext(fileName)
	ret = _FILE_TYPE_INFOS.get(ext)
	if ret is not None:
		return ret

	return _FILE_TYPE_INFO_GENERIC_BINARY
#

FileTypeInfo.guessFromFileName = _guessFromFileName










