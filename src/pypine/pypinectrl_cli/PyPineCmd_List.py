



import os
import sys
import json

import jk_logging
import jk_json

from .PyPineXModuleInfo import PyPineXModuleInfo
from .PyPineXSysInfo import PyPineXSysInfo





class PyPineCmd_List(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self):
		pass
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def command(self) -> str:
		return "list"
	#

	@property
	def description(self) -> str:
		return "List all installed PyPine extensions."
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def run(self, log:jk_logging.AbstractLogger):
		pypinexModuleList = PyPineXSysInfo.installedPackagesList(log)

		for pi in pypinexModuleList:
			print(pi.name, ":", pi.dirPath, ":", pi.meta.version)
	#

#



