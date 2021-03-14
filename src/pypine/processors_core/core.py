


from ..ErrorMode import ErrorMode
from ..FileTypeInfo import FileTypeInfo

from .._Sequence import _Sequence
from .._Chain import _Chain

from .DirScanner import DirScanner
from .FileWriter import FileWriter
from .Noop import Noop
from .Echo import Echo
from .Delete import Delete
from .RunTask import RunTask
from .Cat import Cat
from .ChangeFileName import ChangeFileName
from .SrcFromDict import SrcFromDict






def src(baseDirPath:str, *filePatterns, fileTypeInfo:FileTypeInfo = None):
	return DirScanner(baseDirPath, *filePatterns, fileTypeInfo=fileTypeInfo)
#

def srcFromDict(jData:dict):
	return SrcFromDict(jData)
#

def dest(outputDirPath:str):
	return FileWriter(outputDirPath)
#

def cat():
	return Cat()
#

def noop():
	return Noop()
#

def echo():
	return Echo()
#

def sequence(*producers):
	return _Sequence(*producers)
#

def constructChain(*producers):
	return _Chain(*producers)
#

def delete(bDeleteEmptyDirs:bool = False, errModeDeleteFiles:ErrorMode = ErrorMode.Fail, errModeDeleteDirs:ErrorMode = ErrorMode.Fail):
	return Delete(
		bDeleteEmptyDirs = bDeleteEmptyDirs,
		errModeDeleteFiles = errModeDeleteFiles,
		errModeDeleteDirs = errModeDeleteDirs,
	)
#

def runTask(taskName:str):
	return RunTask(taskName)
#

def changeFileName(
		replaceNameWithIndex:bool = False,
		setExt:str = False,
	):

	return ChangeFileName(replaceNameWithIndex, setExt)
#








