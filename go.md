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
