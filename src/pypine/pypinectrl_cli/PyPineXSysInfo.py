


import os
import sys
import json
import typing

import jk_logging
import jk_json

from .PyPineXModuleInfo import PyPineXModuleInfo






class PyPineXSysInfo(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

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
	def installedPackagesList(log:jk_logging.AbstractLogger = None) -> typing.List[PyPineXModuleInfo]:
		return list(PyPineXSysInfo.installedPackagesIterator(log))
	#

	@staticmethod
	def installedPackagesDict(log:jk_logging.AbstractLogger = None) -> dict:
		pypinexModules = {}

		for pi in PyPineXSysInfo.installedPackagesIterator(log):
			pypinexModules[pi.name] = pi

		return pypinexModules
	#

	@staticmethod
	def installedPackagesPyPiOrgDict(log:jk_logging.AbstractLogger = None) -> dict:
		pypinexModules = {}

		for pi in PyPineXSysInfo.installedPackagesIterator(log):
			pypinexModules[pi.pypiorgName] = pi

		return pypinexModules
	#

	@staticmethod
	def installedPackagesIterator(log:jk_logging.AbstractLogger = None) -> typing.Iterable[PyPineXModuleInfo]:
		modulesEncountered = set()

		for p in sys.path:
			if not os.path.isdir(p):
				continue
			for fe in os.scandir(p):
				if fe.is_dir():
					pi = PyPineXModuleInfo.tryLoad(fe.path, log)
					if pi:
						if pi.name not in modulesEncountered:
							modulesEncountered.add(pi.name)
							yield pi
	#

#









