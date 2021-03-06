



class _TreeLevelComponent(object):

	_ANGLE = "└─"
	_BRANCH = "├─"
	_PASS = "│ "
	_EMPTY = "  "

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self):
		self.__exists = True
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

	def toStrLast(self, bIsLastBranch:bool):
		if not bIsLastBranch:
			return _TreeLevelComponent._BRANCH
		else:
			self.__exists = False
			return _TreeLevelComponent._ANGLE
	#

	def toStr(self):
		if self.__exists:
			return _TreeLevelComponent._PASS
		else:
			return _TreeLevelComponent._EMPTY
	#

#




class TreeHelper(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, prefix:str, levels:list):
		assert isinstance(prefix, str)
		assert isinstance(levels, list)

		self.__prefix = prefix
		self.__levels = levels
		self.rightIsLast = True
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

	def descend(self):
		levels = list(self.__levels)
		levels.append(_TreeLevelComponent())
		return TreeHelper(self.__prefix, levels)
	#

	def toStr(self) -> str:
		if not self.__levels:
			return ""

		ret = [ self.__prefix ]
		for x in self.__levels[:-1]:
			ret.append(x.toStr())
		ret.append(self.__levels[-1].toStrLast(self.rightIsLast))
		return "".join(ret)
	#

#





