## struct memory padding
* to reduce memory padding, order the fields in struct in desc order by size of the field
* but we shouldn't reorder the fields just for memory efficiency. we should order/group the fields for correctness/readability first, unless you have a memory profile tells you that you are using too much of a memory

## struct type conversion
* named struct type needs explicit conversion
* literal struct type can be converted implicitly
