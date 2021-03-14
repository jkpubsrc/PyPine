



import os
import typing

import jk_typing
#import jk_prettyprintobj

from ._INode import _INode
from ._ChainNode import _ChainNode
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

		# build processing chain

		self._nodes = []
		for p in processors:
			if isinstance(p, AbstractProcessor):
				self._nodes.append(_ChainNode(None, p))
			else:
				self._nodes.append(p)
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
		for node in self._nodes:
			node.initialize(ctx)
	#

	def __call__(self, ctx:Context, f):
		for node in self._nodes:
			yield from node(ctx, f)
	#

#






