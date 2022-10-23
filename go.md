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

## value vs pointer
* generally should always use value receiver
* exceptions are unmarshal or decode methods should use pointer receiver
* built-in types use value semantics
* reference types use value semantics except for unmarshal or decode
* struct types we need to make a choice by ourself. e.g. time should be value semantics, and user should be pointer semantcs. If you are not sure, start with pointer semantics
* decoupling will have allocation cost, e.g. f1 := d.displayName, where displayName is a method, we are making indirect reference from f1 -> pointer of d -> real d, and d will be allocated to heap

## atomic instructions vs mutexes
* atomic instructions are faster because they are on the hardware level to take care of synchronization, but it has limitation of only 4 or 8 bytes of memory, so they are great for a single variable, like counter or bool
* when you have a few lines of code need to be synchronized you need to use mutexes

## Race condition
* map could also have race condition even if 2 go routines are writing different values at the same time
* interface could also have race condition, because interface struct is a 2 bytes structure, first byte is the pointer of type of the interface, second byte is the pointer of concrete data. And one gorutine could call the interface function when only half of the interface is updated

## Channel
* Nil -> Send Block, Receive Block
* Open -> Send Allow, Receive Allow
* Closed -> Send Block, Receive Allow
* Signaling with data has to be one goroutine to another, while sginaling without data can be from one gorouting to multiple go routines which is really the channel state change
* Waiting for task: child goroutine is blocked, waiting for task to be passed
* Waiting for result: main goroutine is blocked waiting for the result to be signaled from child goroutine
* Waiting for Finished: use ```ch := make(chan struct{})```, child goroutine call close(ch), and main goroutines will receive siganal wihout data, and unblocked
* Pooling pattern: multiple child goroutines are waiting for tasks to be signaled by doing ``` for p:= range ch ```, when main gorouting send signal to channel, a random child goroutine will receive the signal and do the work
* Fanout semaphore pattern: Use buffered channel to control max concurrent running goroutines. This is another way of reducing the latency in terms of goroutines creation, but at the same time limit the impact that these goroutines are having on another resource
```
sem := make(chan bool, 5)

// in child goroutine
sem <- true // when there is no room is the sem channel, this line will be blocked
code...
<- sem
```
* Drop pattern: use select statement to check if the request can be executed or dropped, select statement is blocked until any case can run
```
sem := make(chan string, 5)

for i := 0; i < 5: i++ {
  go func() {
    for p := range ch {
      fmt.Println("working")
    }
  } ()
}

for i :=0 ; i < 20; i++ {
  select {
  case ch <- "paper":
    fmt.Println("exec")
  default:
    fmt.Println("dropped")
  }
}

```
* Cancellation Pattern (context package): use size 1 buffered channel. But keep in mind that we have to use buffered channel. If you use unbuffered channel. What will happen is that when tc sends signal, the main goroutine continues to run and finished, and then the child goroutine finished and tries to send the signal, there is no receiver anymore (since unbuffered channel needs to have both sender and receiver at the same time), and child goroutine will be blocked forever, and this is **a classic goroutine leak**. With buffered channel, no need to have a receiver ready.
```
ch := make(channel string, 1)

go func () {
  time.Sleep(time.Duration(rand.Intn(500) * time.Millisecond)
  ch <- "paper"
} ()

tc := time.After(100 * time.Millisecond // return a channel that will send signal after 100 milli seconds)

select {
case p := <-ch:
  fmt.Println("recv")
case t := <-tc:
  fmt.Println("timeout")
{

```
## Context
* after adding a key value pair to the context, when retrieving it, need to use the same key type.
```
const traceIDKey TraceIDKey = 0

ctx := context.WithValue(context.Background(), traceIDKey, "afee97f3-3e97-425e-96ee-6c48e1f39c2d")

ctx.Value(traceIDKey).(TraceID) // work
ctx.Value(0).(TraceID) // does not work
```
* ctx.Done() returns a channel that will close (send signal without data) when the timeout has passed
```
duration := 150 * time.Millisecond

ctx, cancel := context.WithTimeout(context.Background(), duration)
defer cancel() // calling cancel will immediate terminate the function and relase the resources, and calling cancel twice is ok. That's why we always call cancel regardless

ch := make(chan data, 1)

go func() {
  time.Sleep(500 * time.Millisecond)
  
  ch <- data("123")
} ()

select {
case d := <- ch:
  fmt.Println("work done")
  
case <-ctx.Done():
  fmt.Println("canceled")
}

```
## Concurrency vs Parallelism
* currency is a property of the code; parallelism is property of the running program
* we write correnty code that we hope will be run in parallel (if one core no parallelism, when multiple cores we have parallelism) 
