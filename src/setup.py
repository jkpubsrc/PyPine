################################################################################
################################################################################
###
###  This file is automatically generated. Do not change this file! Changes
###  will get overwritten! Change the source file for "setup.py" instead.
###  This is either 'packageinfo.json' or 'packageinfo.jsonc'
###
################################################################################
################################################################################


from setuptools import setup

def readme():
	with open("README.md", "r", encoding="UTF-8-sig") as f:
		return f.read()

setup(
	author = "Jürgen Knauth",
	author_email = "pubsrc@binary-overflow.de",
	classifiers = [
		"Development Status :: 3 - Alpha",
		"License :: OSI Approved :: Apache Software License",
		"Programming Language :: Python :: 3",
	],
	description = "A Python based build and data processing framework.",
	include_package_data = False,
	install_requires = [
		"requests",
		"jk_typing",
		"jk_flexdata",
		"jk_json",
		"jk_logging",
		"jk_prettyprintobj",
		"jk_pathpatternmatcher2",
		"jk_argparsing",
		"jk_pypiorgapi",
		"jk_utils",
	],
	keywords = [
		"pypine",
		"build",
	],
	license = "Apache2",
	name = "pypine",
	packages = [
		"pypine",
		"pypine.do",
		"pypine.utils",
		"pypine.processors_core",
		"pypine.pypinectrl_cli",
	],
	scripts = [
		"bin/pypinectrl.py",
	],
	version = "0.2021.3.19",
	zip_safe = False,
	long_description = readme(),
	long_description_content_type="text/markdown",
)
