

import os

import jk_json
import jk_flexdata
import jk_logging




class PyPineXModuleInfo(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, dirPath:str, jInfo:dict):
		self.name = os.path.basename(dirPath)
		self.pypiorgName = self.name.replace("_", "-")
		self.dirPath = dirPath
		self.meta = jk_flexdata.FlexObject(jInfo["meta"])
		self.compatibility = jk_flexdata.FlexObject(jInfo["compatibility"])
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

	@staticmethod
	def tryLoad(dirPath:str, log:jk_logging.AbstractLogger = None):
		pypinexInfoFilePath = os.path.join(dirPath, "pypinex_info.json")
		if not os.path.isfile(pypinexInfoFilePath):
			return None

		moduleName = os.path.basename(dirPath)

		try:
			jData = jk_json.loadFromFile(pypinexInfoFilePath)
		except Exception as ee:
			if log:
				log.error(ee)
			return None

		# check format

		try:
			if not jData["magic"]["magic"] == "pypinex-info":
				raise Exception()
			if jData["magic"]["version"] != 1:
				raise Exception()
		except Exception as ee:
			if log:
				log.error("Not a valid PyPine extension file!")
			return None

		# create instance of PyPineXModuleInfo

		return PyPineXModuleInfo(dirPath, jData)
	#

#






