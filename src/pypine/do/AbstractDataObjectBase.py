





import os

from ._CommonDataObjectMixin import _CommonDataObjectMixin







#
# This is an abstract base class for implementing data objects.
# If you want to implement new data objects you might want to start from here.
#
class AbstractDataObjectBase(_CommonDataObjectMixin):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, relFilePath:str):
		assert isinstance(relFilePath, str)
		assert relFilePath

		self._relFilePath = relFilePath
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def relFilePath(self) -> str:
		return self._relFilePath
	#

	@property
	def isLocal(self) -> bool:
		return True
	#

	@property
	def isLocalOnDisk(self) -> bool:
		return False
	#

	@property
	def relDirPath(self) -> str:
		return os.path.dirname(self._relFilePath)
	#

	#
	# The name of this data object
	#
	@property
	def fileName(self) -> str:
		return os.path.basename(self._relFilePath)
	#

	################################################################################################################################
	# definitively overwrite

	@property
	def fileTypeInfo(self):
		raise NotImplementedError()
	#

	@property
	def dataType(self) -> str:
		raise NotImplementedError()
	#

	################################################################################################################################
	# maybe overwrite

	@property
	def baseDirPath(self) -> str:
		return None
	#

	#
	# This is the absolute path of this entry.
	#
	@property
	def fullPath(self) -> str:
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

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

#











