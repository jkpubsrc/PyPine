



import re
import typing
import os
import datetime

import jk_typing







def _toStr0(number:int, lengthInCharacters:int):
	s = str(number)
	while len(s) < lengthInCharacters:
		s = "0" + s
	return s
#


_allKeys = [
	"%Y",
	"%m",
	"%d",
	"%H",
	"%M",
	"%S",
	"$(year)",
	"$(month)",
	"$(day)",
	"$(hour)",
	"$(minute)",
	"$(second)",
	"$(millis)",
	"$(relDirPath)",
	"$(relFilePath)",
	"$(relFilePathWithoutExt)",
	"$(fileName)",
	"$(fileExt)",
	"$(fileNameWithoutExt)",
]
_sStr = "|".join([
	key.replace("$(", "\\$\\(").replace(")", "\\)") for key in _allKeys
])
_varSplitPattern = re.compile("(" + _sStr + ")")





class RelFilePathBuilder(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, filePathPattern:str):
		self.__timestamp = datetime.datetime.now()

		_year = _toStr0(self.__timestamp.year, 4)
		_month = _toStr0(self.__timestamp.month, 2)
		_day = _toStr0(self.__timestamp.day, 2)
		_hour = _toStr0(self.__timestamp.hour, 2)
		_minute = _toStr0(self.__timestamp.minute, 2)
		_second = _toStr0(self.__timestamp.second, 2)
		_millis = _toStr0(self.__timestamp.microsecond // 1000, 4)

		self.__xvars = {
			"%Y": _year,
			"%m": _month,
			"%d": _day,
			"%H": _hour,
			"%M": _minute,
			"%S": _second,
			"$(year)": _year,
			"$(month)": _month,
			"$(day)": _day,
			"$(hour)": _hour,
			"$(minute)": _minute,
			"$(second)": _second,
			"$(millis)": _millis,
		}

		self.__pattern = []
		for p in _varSplitPattern.split(filePathPattern):
			if not p:
				continue
			if p in self.__xvars:
				self.__pattern.append(self.__xvars[p])
			else:
				self.__pattern.append(p)
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

	def buildFilePath(self, f) -> str:
		xvars2 = {
			"$(relDirPath)": f.relDirPath,
			"$(relFilePath)": f.relFilePath,
			"$(relFilePathWithoutExt)": f.relFilePathWithoutExt,
			"$(fileName)": f.fileName,
			"$(fileExt)": f.fileExt,
			"$(fileNameWithoutExt)": f.fileNameWithoutExt,
		}

		ret = []
		for p in self.__pattern:
			if p in xvars2:
				ret.append(xvars2[p])
			else:
				ret.append(p)

		s = "".join(ret)
		if s.startswith("/"):
			return s[1:]
		else:
			return s
	#

#