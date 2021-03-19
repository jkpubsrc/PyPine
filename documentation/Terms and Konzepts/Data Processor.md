The Concept
================================================================

A data processor is a software component that receives input data objects, processes the data objects and produces output data objects.
By definition there is no specific numerical correlation between
input and output, which means: A processor can receive no (real) input and produce many output data objects, or it can receive
a lot of input data objects but produce just one or even no output data object.

However, the following scenarios are typical for data processors:

* for every input data object received, produce exactly one corresponding output data object (-> e.g. a data converter)
* for a single data object and produce a large variety of output data objects (-> e.g. to feed data into a pipeline)
* for a large amount of input data objects produce exactly one output data object (-> e.g. to merge multiple data objects to a single one)

The Implementation
================================================================

A data processor is implemented by deriving from `AbstratProcessor`. It follows the semantic desribed next.

* If a task is about to run, `initializeProcessing(ctx)` will be invoked.
* For every data object received `processElement(ctx, f)` is invoked.
	* If this is the very first processor in a pipeline, a `None` is passed to this method.
	* Here the processor can return a single data object using `return`, a variety of data objects using `yield`, or even not return anything (which es equivalent to returning `None`).
* After all data provided by `processElement(ctx, f)` has been processed, `processingCompleted(ctx)` will be invoked.
	* Here the processor can return a single data object using `return`, a variety of data objects using `yield`, or even not return anything (which es equivalent to returning `None`).




