#!/usr/bin/python



import os
import typing
import sys

import jk_typing
#import jk_prettyprintobj
import jk_argparsing






ap = jk_argparsing.ArgsParser(os.path.basename(__file__), "PyPine scripting manager.")

# ---

ap.optionDataDefaults.set("help", False)

# ---

ap.createOption("h", "help", "Display this help text.").onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("help", True)

ap.createCommand("help", "Displays this help text.")

ap.createAuthor("Jürgen Knauth", "jk@binary-overflow.de", "PyPine framework")

# ---

parsedArgs = ap.parse()

if not parsedArgs.programArgs or ("help" in parsedArgs.programArgs) or parsedArgs.optionData["help"]:
	ap.showHelp()
	sys.exit(0)




