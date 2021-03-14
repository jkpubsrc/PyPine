



import os
import typing

import jk_typing
#import jk_prettyprintobj

from ._INode import _INode
from ._ChainNode import _ChainNode
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
		assert processors
		for x in processors:
			assert isinstance(x, (AbstractProcessor, _INode))
		self._processors = processors

		# build processing chain

		lastNode = None
		for p in processors:
			if isinstance(p, AbstractProcessor):
				lastNode = _ChainNode(lastNode, p)
			else:
				lastNode = p
		self._nodes = lastNode
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

	@jk_typing.checkFunctionSignature()
	def initialize(self, ctx:Context):
		self._nodes.initialize(ctx)
	#

	def __call__(self, ctx:Context, f):
		yield from self._nodes(ctx, f)
	#

#






