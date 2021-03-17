#!/usr/bin/python3



import os
import typing
import sys

import jk_typing
#import jk_prettyprintobj
import jk_argparsing
import jk_argparsing.textmodel
import jk_logging

import pypine
import pypine.pypinectrl_cli









ap = jk_argparsing.ArgsParser(os.path.basename(__file__), "This is the PyPine management tool. It supports installing and managing PyPine scripts.")

# ---

ap.optionDataDefaults.set("help", False)

# ---

ap.createSynopsis("pypinectrl.py <command>")

ap.createOption("h", "help", "Display this help text.").onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("help", True)

ap.createCommand("help", "Displays this help text.")

ap.createAuthor("Jürgen Knauth", "jk@binary-overflow.de", "PyPine framework")

ap.setLicense("Apache")

ap.addExtraChapterEnd(jk_argparsing.textmodel.TSection(
	"More Information", [
		"More information about PyPine can be found here:",
		jk_argparsing.textmodel.TSection(
			"The Project", [
				"* https://pypine.binary-overflow.de :: The PyPine main site",
				"* https://github.com/jkpubsrc/pypine/ :: The Source code",
				"* https://pypi.org/project/pypine/ :: The Python package on pypi.org",
			],
		),
		jk_argparsing.textmodel.TSection(
			"Extensions", [
			],
		),
		jk_argparsing.textmodel.TSection(
			"Documentation and Examples", [
			],
		),
	]
))

# ----

cmds = {}
def registerCmd(clazz):
	c = clazz()
	ap.createCommand(c.command, c.description)
	cmds[c.command] = c
#

registerCmd(pypine.pypinectrl_cli.PyPineCmd_List)
registerCmd(pypine.pypinectrl_cli.PyPineCmd_Search)

# ---

ap.installLocalBashCompletion(os.path.abspath(__file__))

# ---

parsedArgs = ap.parse()

if not parsedArgs.programArgs or ("help" in parsedArgs.programArgs) or parsedArgs.optionData["help"]:
	ap.showHelp()
	sys.exit(0)

with jk_logging.wrapMain() as log:

	for programArg in parsedArgs.programArgs:
		c = cmds.get(programArg)
		if c is None:
			log.error("No such command: " + programArg)
		else:
			c.run(log)

#

