



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

	@property
	def fileNameWithoutExt(self) -> str:
		return self.fileName[:len(self.fileExt)]
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
		return self.relFilePath[:len(self.fileExt)]
	#

#





