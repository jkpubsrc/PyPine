



import os
import typing

import jk_typing
#import jk_prettyprintobj

from ._INode import _INode
from ._ChainNodeP import _ChainNodeP
from ._Sequence import _Sequence
from .Context import Context
from .AbstractProcessor import AbstractProcessor
from .utils.TreeHelper import TreeHelper
from .utils.Color import Color





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
			assert isinstance(x, (AbstractProcessor, _Sequence))

		# build processing chain

		previousNode = None
		for p in processors:
			if isinstance(p, _Sequence):
				p._prevChainNode = previousNode
				previousNode = p
			else:
				previousNode = _ChainNodeP(previousNode, p)
		self.__node = previousNode
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dump(self, th:TreeHelper):
		print(Color.BLUE + th.toStr() + "Chain" + Color.RESET)

		th = th.descend()
		th.rightIsLast = True

		self.__node._dump(th)
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def initialize(self, ctx:Context):
		self.__node.initialize(ctx)
	#

	def __call__(self, ctx:Context, f):
		yield from self.__node(ctx, f)
	#

#






