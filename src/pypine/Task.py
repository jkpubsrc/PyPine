



import datetime
import os
import typing

import jk_typing
#import jk_prettyprintobj

from ._INode import _INode
from .Context import Context
from .utils.Color import Color
from .utils.ObservableEvent import ObservableEvent
from .utils.TreeHelper import TreeHelper






class Task(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, name, chain:_INode):
		self.__name = name
		self.__chain = chain

		self.__onStarted = ObservableEvent("onStarted")
		self.__onCompleted = ObservableEvent("onCompleted")
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def name(self) -> str:
		return self.__name
	#

	@property
	def onStarted(self) -> ObservableEvent:
		return self.__onStarted
	#

	@property
	def onCompleted(self) -> ObservableEvent:
		return self.__onCompleted
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def dump(self):
		print(Color.LIGHT_CYAN + "Task:" + repr(self.__name) + Color.RESET)
		th = TreeHelper("  ", [])
		th = th.descend()
		th.rightIsLast = True
		self.__chain._dump(th)
	#

	@jk_typing.checkFunctionSignature()
	def run(self, ctx:Context, taskName:str, f):
		if taskName:
			ctx.printTaskBegin("Running task '{}' ...".format(taskName))
		else:
			ctx.printTaskBegin("Running task ...")

		t0 = datetime.datetime.now()

		self.__chain.initialize(ctx)

		self.__onStarted.fire(self, ctx)

		lastF = None
		for nextF in self.__chain(ctx, f):
			lastF = nextF

		# TODO: cleanup the context!

		self.__onCompleted.fire(self, ctx, lastF)

		dur = (datetime.datetime.now() - t0).total_seconds()
		if taskName:
			ctx.printTaskSucceeded("Completed task '{}' after {:.2f} seconds.".format(taskName, dur))
		else:
			ctx.printTaskSucceeded("Completed after {:.2f} seconds.".format(dur))

		return lastF
	#

#





