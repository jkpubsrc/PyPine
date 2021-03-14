


import os
import typing

import jk_typing
#import jk_prettyprintobj

from ._INode import _INode
from .EnumAction import EnumAction
from .FileTypeInfo import FileTypeInfo
from .Context import Context
from .AbstractProcessor import AbstractProcessor








class _ChainNode(_INode):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self, lastChainNode:typing.Union[_INode,None], processor:AbstractProcessor):
		if lastChainNode is not None:
			assert callable(lastChainNode)
		self._prevChainNode = lastChainNode

		if getattr(processor, "_bConstructorCalled", None) is not True:
			raise Exception("Please use super().__init__() to invoke the constructor of the base class in your implementation of " + processor.__class__.__name__ + ".__init__()!")
		self._processor = processor
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Methods to Override
	################################################################################################################################

	def __runProcessor_processElement(self, ctx:Context, f):
		# verify the input object

		if not self._processor.isProcessable(f):
			# this data type can not be handled by this processor!
			if self._processor._actionIfUnprocessable == EnumAction.Ignore:
				yield f
			elif self._processor._actionIfUnprocessable == EnumAction.Warn:
				ctx.printVerbose(None, "Input for {} not of types {} => Ignoring: {}", self._processor.processorTypeName, self._processor_processableDataTypes_s, f.relFilePath)
				yield f
			elif self._processor._actionIfUnprocessable == EnumAction.Fail:
				raise Exception("Input for {} not of types {}!".format(self._processor.processorTypeName, self._processor_processableDataTypes_s))

		# now process the object

		ret = self._processor.processElement(ctx, f)

		# return the object or objects created

		if hasattr(ret, "__iter__"):
			for x in ret:
				if x is not None:
					yield x
		else:
			if ret is not None:
				yield ret
	#

	def __runProcessor_processingCompleted(self, ctx:Context):
		ret = self._processor.processingCompleted(ctx)
		if hasattr(ret, "__iter__"):
			for x in ret:
				if x is not None:
					yield x
		else:
			if ret is not None:
				yield ret
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def initialize(self, ctx:Context):
		if self._prevChainNode:
			self._prevChainNode.initialize(ctx)
		self._processor.initialize(ctx)
	#

	def __call__(self, ctx:Context, f):
		if not self._processor.isInitialized:
			raise jk_utils.ImplementationError()

		if self._prevChainNode is None:
			yield from self.__runProcessor_processElement(ctx, f)
		else:
			for f2 in self._prevChainNode(ctx, f):
				yield from self.__runProcessor_processElement(ctx, f2)
		yield from self.__runProcessor_processingCompleted(ctx)
	#

#






