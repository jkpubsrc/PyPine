


import os
import typing

import jk_typing
import jk_utils
#import jk_prettyprintobj

from .utils.TreeHelper import TreeHelper
from ._INode import _INode
from .EnumAction import EnumAction
from .FileTypeInfo import FileTypeInfo
from .Context import Context
from .AbstractProcessor import AbstractProcessor
from .utils.Color import Color








class _ChainNodeP(_INode):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self, prevChainNode:typing.Union[_INode,None], processor:AbstractProcessor):
		if prevChainNode is not None:
			assert callable(prevChainNode)
		self._prevChainNode = prevChainNode

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

	#
	# Yields data objects provided by a processor.
	#
	def __runProcessor_processElement(self, ctx:Context, f):
		# verify the input object

		if not self._processor.isProcessable(f):
			# this data type can not be handled by this processor!
			if self._processor._actionIfUnprocessable == EnumAction.Ignore:
				yield f
			elif self._processor._actionIfUnprocessable == EnumAction.Warn:
				ctx.printVerbose(None, "Input for {} is not processable => Ignoring: {}", self._processor.processorTypeName, repr(f))
				yield f
			elif self._processor._actionIfUnprocessable == EnumAction.Fail:
				raise Exception("Input for {} is not processable: {}!".format(self._processor.processorTypeName, repr(f)))

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

	#
	# Yields data objects provided by a processor.
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

	def _dump(self, th:TreeHelper):
		s = self._processor.processorDetailsHR
		if s:
			s = Color.YELLOW + self._processor.processorTypeName + "⧼" + Color.WHITE + s + Color.YELLOW + "⧽"
		else:
			s = Color.YELLOW + self._processor.processorTypeName

		print(Color.BLUE + th.toStr() + s + Color.RESET)

		if self._prevChainNode:
			th = th.descend()
			th.rightIsLast = True
			self._prevChainNode._dump(th)
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

	#
	# Yields data objects provided by a processor.
	# First all regularly provided data objects are returned, then the 'completed' data objects.
	#
	def __call__(self, ctx:Context, f):
		if not self._processor.isInitialized:
			raise jk_utils.ImplementationError()

		if self._prevChainNode is None:
			yield from self.__runProcessor_processElement(ctx, f)
		else:
			for f2 in self._prevChainNode(ctx, f):
				if f2 is not None:
					yield from self.__runProcessor_processElement(ctx, f2)
		yield from self.__runProcessor_processingCompleted(ctx)
	#

#






