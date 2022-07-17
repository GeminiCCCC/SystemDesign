# 1. single machine

a. use hash table.  
b. to fit more data we can use data compression or onlyu store frequently used data in memory and the rest on disg

# 2. use vector clock to solve data inconsistency

a. D1([Sx, 1]) -> D2([Sx, 2] -> D3([Sx, 2], [Sy, 1]) / D4([Sx, 2], [Sz, 1]) -> D5([Sx3, [Sy, 1], [Sz, 1]), when reads D3 and D4, it discovers a conflict. Then the conflict is resolved by the client and updated date is sent to the server, assume the write is handled by Sx. 

b. two downsides: first it adds complexity to client who will need to implement conflict resolution logic. Second the [server: version] pairs could grow rapidly. To fix this we can set a threshold for the length and remove old pairs when it exceedes the limit. This can lead to inefficiencies in reconciliation because the descendant relationship cannot be determined accurately. However, based on Dynamo paper, Amazon has not yet encountered this problem in production
