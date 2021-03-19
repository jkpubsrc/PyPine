#!/usr/bin/python3




from pypine import *





tasks = Tasks()





tasks.add("hello_world", "A 'Hello, World!' PyPine script.", [
		core.src(".", "hello_world.txt"),
		core.cat(),
	]
)




tasks.run("hello_world")






