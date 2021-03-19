



import os
import typing

import jk_typing
#import jk_prettyprintobj

from ._INode import _INode
from ._ChainNodeP import _ChainNodeP
from .Context import Context
from .AbstractProcessor import AbstractProcessor






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

	def _dump(self, prefix:str, prefix2:str):
		print(prefix + "└─Sequence")

		if self._prevChainNode is None:
			prefix2 = prefix + "  ├"
			prefix2b = prefix + "  │"
			prefix3 = prefix + "  └"
			prefix3b = prefix + "   "
		else:
			prefix2 = prefix + "  ├"
			prefix2b = prefix + "  │"
			prefix3 = prefix + "  └"
			prefix3b = prefix + "   "

		for i, node in enumerate(reversed(self._nodes)):
			bLast = i == len(self._nodes) - 1
			if not bLast:
				node._dump(prefix2, prefix2b)
			else:
				node._dump(prefix3, prefix3b)

		if self._prevChainNode is not None:
			self._prevChainNode._dump(prefix + "  ", prefix + "  ")
			pass
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






