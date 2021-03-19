#!/usr/bin/python3




from pypine import *
import pypinex_pack as pack




tasks = Tasks()





tasks.add("demo", "A demonstration PyPine script for chains and sequences.", [
		core.src(".", "foo_bar.txt"),
		core.sequence(
			core.constructChain(
				core.src(".", "hello_world.txt"),
				core.echo(),
			),
			core.src(".", "the_quick.txt"),
		),
		core.echo(),
	]
)




tasks.getE("demo").dump()
print()

tasks.run("demo")






