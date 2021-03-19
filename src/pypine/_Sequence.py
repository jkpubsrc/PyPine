



import os
import typing

import jk_typing
#import jk_prettyprintobj

from .utils.TreeHelper import TreeHelper
from ._INode import _INode
from ._ChainNodeP import _ChainNodeP
from .Context import Context
from .AbstractProcessor import AbstractProcessor
from .utils.Color import Color






class _Sequence(_INode):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, *processors):
		assert processors
		for p in processors:
			assert isinstance(p, (AbstractProcessor, _INode))
		self._processors = processors

		self._prevChainNode = None

		# build processing chain

		self._nodes = []
		for p in processors:
			if isinstance(p, AbstractProcessor):
				self._nodes.append(_ChainNodeP(None, p))
			else:
				self._nodes.append(p)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dump(self, th:TreeHelper):
		print(Color.BLUE + th.toStr() + "Sequence" + Color.RESET)

		th = th.descend()
		for i, node in enumerate(reversed(self._nodes)):
			th.rightIsLast = (self._prevChainNode is None) and (i == len(self._nodes) - 1)
			node._dump(th)

		if self._prevChainNode is not None:
			th.rightIsLast = True
			self._prevChainNode._dump(th)
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def initialize(self, ctx:Context):
		for node in self._nodes:
			node.initialize(ctx)
		if self._prevChainNode is not None:
			self._prevChainNode.initialize(ctx)
	#

	def __call__(self, ctx:Context, f):
		if self._prevChainNode is None:
			for node in self._nodes:
				yield from node(ctx, f)
		else:
			yield from self._prevChainNode(ctx, f)
			for node in self._nodes:
				yield from node(ctx, None)
	#

#






