## struct memory padding
* to reduce memory padding, order the fields in struct in desc order by size of the field
* but we shouldn't reorder the fields just for memory efficiency. we should order/group the fields for correctness/readability first, unless you have a memory profile tells you that you are using too much of a memory

## struct type conversion
* named struct type needs explicit conversion
* literal struct type can be converted implicitly

## Stack, Heap
* each thread will be allocated to 1M size of stack
* each goroutine will also be allocated to 2k size of stack
* whenever return &u, the struct u will be allocated in heap instead of stack, because stack memory will be self-cleaned once the function is returned. And allocation in heap comes with a cost which is garbage collection

## Array, slice
* array is very efficient because it creates predictable access pattern which will preload data into the processor before we need it. and L1, L2 caches inside precessor is much faster than the main memory. Because go is not working on a virtual machine like JVM, it directly works with the machine which is the processor. That's why it's so important to optimize for predicatable access pattern, and linked list, queue, stack are not so great of doing it.
* 2 index slicing is dangerous when you need to do append on the sliced array, since they will be sharing the same back array in heap, because append will not allocate new array in heap when len < cap. What you can do is to use 3rd index to set max the same is the end, a[1:4] -> a[1:4:4], this is because when len = cap, it will allocate a new array in heap, which means the change on the sliced array will not affect the original one
* Range on slice has both value and pointer semantics. for i := range nums is pointer sementics which means it directly iterates on the original slice. for i, v := range nums is value sementics which means it makes a copy of original slices and iterate on the copied one, and keep in mind slices are 3 bytes structure, first byte is a pointer pointing to the backing array in the heap, second byte is the length, third byte is the capacity.
