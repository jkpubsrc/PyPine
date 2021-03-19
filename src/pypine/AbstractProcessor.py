


import os
import typing

import jk_typing

from .EnumAction import EnumAction
from .FileTypeInfo import FileTypeInfo
from .Context import Context









class AbstractProcessor(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self, actionIfUnprocessable:bool = EnumAction.Warn):
		assert isinstance(actionIfUnprocessable, EnumAction)

		self._ctx = None
		self._bConstructorCalled = True
		self._bInitialized = False
		self._actionIfUnprocessable = actionIfUnprocessable

		s = self.__class__.__name__
		self.__processorTypeName = s[0].lower() + s[1:]
	#

	@jk_typing.checkFunctionSignature()
	def initialize(self, ctx:Context):
		if getattr(self, "_bConstructorCalled", None) is not True:
			raise Exception("Please use super().__init__() to invoke the constructor of the base class in your implementation of " + self.__class__.__name__ + ".__init__()!")

		self._ctx = ctx
		self._bInitialized = True
		self.initializeProcessing(ctx)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def isInitialized(self) -> bool:
		return self._bInitialized
	#

	@property
	def processorTypeName(self) -> str:
		return self.__processorTypeName
	#

	@property
	def processorDetailsHR(self) -> str:
		return None
	#

	@property
	def actionIfUnprocessable(self) -> EnumAction:
		return self._actionIfUnprocessable
	#

	@actionIfUnprocessable.setter
	def actionIfUnprocessable(self, action:EnumAction):
		assert isinstance(action, EnumAction)
		self._actionIfUnprocessable = action
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def setActionIfUnprocessable(self, action:EnumAction):
		assert isinstance(action, EnumAction)
		self._actionIfUnprocessable
		return self
	#

	################################################################################################################################
	## Methods to Override
	################################################################################################################################

	def isProcessable(self, f) -> bool:
		if f is None:
			return False
		pList = self.processableDataTypes()
		if pList is None:
			return True
		assert isinstance(pList, (tuple, list))
		return f.dataType in pList
	#

	def processableDataTypes(self) -> typing.Union[list,None]:
		return None
	#

	def initializeProcessing(self, ctx:Context):
		pass
	#

	def processElement(self, ctx:Context, f):
		pass
	#

	def processingCompleted(self, ctx:Context):
		pass
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

#






