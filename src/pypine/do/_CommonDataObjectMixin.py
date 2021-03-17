



import os




#
# Expected existing variables or properties:
# * str fileName
# * str relFilePath
#
class _CommonDataObjectMixin():

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def fileNameWithoutExt(self) -> str:
		ext = self.fileExt
		return self.fileName[:-len(ext)]
	#

	@property
	def fileExt(self) -> str:
		baseFileName, ext = self.__splitExt(self.fileName)

		if ext in ( ".gz", ".bz2", ".xz" ):
			baseFileName2, ext2 = self.__splitExt(baseFileName)
			if ext2 == ".tar":
				return ".tar" + ext

		return ext
	#

	@property
	def relFilePathWithoutExt(self) -> str:
		ext = self.fileExt
		return self.relFilePath[:-len(ext)]
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	#
	# * "" => ("", "")
	# * "foo.txt" => ("foo", ".txt")
	# * "foo." => ("foo", ".")
	# * "foo.bar.txt" => ("foo.bar", ".txt")
	# * ".bar" => (".bar", "")
	# * "bar" => ("bar", "")
	#
	def __splitExt(self, fn:str) -> str:
		if not fn:
			return "", ""

		pos = fn.rfind(".")
		if pos > 0:
			return fn[:pos], fn[pos:]
		else:
			return fn, ""
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def __str__(self):
		return "{}<({} :: {})>".format(self.__class__.__name__, repr(self.relFilePath), self.fileTypeInfo)
	#

	def __repr__(self):
		return "{}<({} :: {})>".format(self.__class__.__name__, repr(self.relFilePath), self.fileTypeInfo)
	#

#





