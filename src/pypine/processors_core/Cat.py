



import os
import typing

import jk_utils

from ..FileTypeInfo import FileTypeInfo
from ..do.DiskFile import DiskFile
from ..do.InMemoryFile import InMemoryFile
from ..Context import Context
from ..AbstractProcessor import AbstractProcessor






class Cat(AbstractProcessor):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self):
		super().__init__()
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

	def isProcessable(self, f) -> bool:
		return True
	#

	def processElement(self, ctx:Context, f):
		ctx.printDetail(self, "=" * 120)

		if f is None:
			ctx.printDetail(self, "(none)")

		else:
			ctx.printDetail(self, ctx.__class__.__name__ + ": " + f.relFilePath)
			ctx.printDetail(self, "Size: " + jk_utils.formatBytes(f.getFileSize()))
			ctx.printDetail(self, "isBinary: " + str(f.isBinary))
			ctx.printDetail(self, "isText: " + str(f.isText))
			ctx.printDetail(self, "-" * 120)

			if getattr(f, "isText", False):
				text = f.readText()
				for s in text.split("\n"):
					ctx.printDetail(self, s)

			elif getattr(f, "isBinary", False):
				hexRowSize = 16

				raw = f.readBinary()
				sRawHex = raw.hex()
				n = len(raw)
				i = 0
				bufHex = []
				bufASCII = []
				while i < n:
					addr = i.to_bytes(4, byteorder="big").hex()
					for j in range(0, hexRowSize):
						iPos1 = i + j
						iPos2 = iPos1*2

						if iPos1 < n:
							bufHex.append(sRawHex[iPos2:iPos2+2])
							c = raw[iPos1]
							if 32 <= c <= 126:
								bufASCII.append(chr(c))
							else:
								bufASCII.append(".")
						else:
							bufHex.append("  ")
							bufASCII.append(" ")

					s = addr + "    " + " ".join(bufHex) + "    |" + "".join(bufASCII) + "|"
					ctx.printDetail(self, s)

					i += hexRowSize*2
					bufHex.clear()
					bufASCII.clear()

			else:
				ctx.printDetail(self, "(unknown content)")

		ctx.printDetail(self, "=" * 120)
		return f
	#

#






