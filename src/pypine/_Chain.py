



import os
import typing

import jk_typing
#import jk_prettyprintobj

from ._INode import _INode
from ._ChainNodeP import _ChainNodeP
from ._Sequence import _Sequence
from .Context import Context
from .AbstractProcessor import AbstractProcessor






class _Chain(_INode):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, *processors):
		print("----")
		print(processors)
		print("----")

		assert processors
		for x in processors:
			assert isinstance(x, (AbstractProcessor, _Sequence))
		self._processors = processors

		# build processing chain

		previousNode = None
		for p in processors:
			if isinstance(p, _Sequence):
				p._prevChainNode = previousNode
				previousNode = p
			else:
				previousNode = _ChainNodeP(previousNode, p)
		self._nodes = previousNode
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dump(self, prefix:str="", prefix2:str=""):
		print(prefix + "─Chain")
		self._nodes._dump(prefix2 + " ")
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def initialize(self, ctx:Context):
		self._nodes.initialize(ctx)
	#

	def __call__(self, ctx:Context, f):
		yield from self._nodes(ctx, f)
	#

#






