# 1. single machine

a. use hash table.  
b. to fit more data we can use data compression or onlyu store frequently used data in memory and the rest on disg

# 2. use vector clock to solve data inconsistency

a. D1([Sx, 1]) -> D2([Sx, 2] -> D3([Sx, 2], [Sy, 1]) / D4([Sx, 2], [Sz, 1]) -> D5([Sx3, [Sy, 1], [Sz, 1]), when reads D3 and D4, it discovers a conflict. Then the conflict is resolved by the client and updated date is sent to the server, assume the write is handled by Sx. 

b. two downsides: first it adds complexity to client who will need to implement conflict resolution logic. Second the [server: version] pairs could grow rapidly. To fix this we can set a threshold for the length and remove old pairs when it exceedes the limit. This can lead to inefficiencies in reconciliation because the descendant relationship cannot be determined accurately. However, based on Dynamo paper, Amazon has not yet encountered this problem in production

# 3. gossip protocal to detect failure

a. each node maintains a node membership list, which contains member IDs and heartbeat counters.  
b. each node periodically increments its heartbeat counter.  
c. each node periodically sends heatbeats to a set of random nodes, which in turn propagate to another set of nodes.  
d. once nodes receive heartbeats, membership list is updated to the latest info.  
e. if the heatbeat has not increased for more thana predefined periods, the member is considered as offline.  

# 4. use sloppy quorum to improve availability when temporary failures happen

a. after nodes are down instead of enforcing the quorum requirement, the system chooses the first W healthy servers for writes and first R healthy servers for reads on the hash ring.

# 5. use Merkle tree is handle replica permanently failure (to keep replicas in sync)
* step 1: divide key space into buckets which will be used in leaf nodes. 
* step 2: hash each key
* step 3: create a single hash node per bucket
* step 4: build the tree upwards till root by calculating hashed of children

To compare two Merkle trees, start by comparing root hashes. If root hashes match, both servers have the same data, otherwise traverse the tree to find the which buckets are not synchronized and synchronize those buckets only. So the amount of data needed to be synchronized is proportional to the differences, and not the amount of data.
