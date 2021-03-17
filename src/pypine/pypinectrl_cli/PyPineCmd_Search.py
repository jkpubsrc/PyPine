



import os
import sys
import json

import jk_logging
import jk_json
import jk_pypiorgapi

from .PyPineXModuleInfo import PyPineXModuleInfo
from .PyPineXSysInfo import PyPineXSysInfo







class PyPineCmd_Search(object):

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
		return "search"
	#

	@property
	def description(self) -> str:
		return "Search pypi.org for more packages."
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def run(self, log:jk_logging.AbstractLogger):
		pypinexModuleDict = PyPineXSysInfo.installedPackagesPyPiOrgDict(log)

		api = jk_pypiorgapi.PyPiOrgAPI()

		for n, nMax, pkgName, pkgVersion, pkgDescription in api.iteratePackagesByClassifier("pypinex", [
				"Environment :: Plugins",
				"Programming Language :: Python :: 3",
				"Topic :: Utilities",
			], log):

			pkgInfo = pypinexModuleDict.get(pkgName)
			if pkgInfo:
				installedPkgVersion = pkgInfo.meta.version
			else:
				installedPkgVersion = ""

			print((n, nMax, pkgName, pkgVersion, installedPkgVersion, pkgDescription))
	#

#



