## Multi-master replication

a. use databases auto_increment feature, each database increase it by k, where k is the number of database servers in use.  
b. but cannot scale and will have issue when a server is added or removed

## UUID

a. IDs are 128 bits long, but our requirement might be 64 bits.  
b. do not go up with time.  
c. non-numeric

## Ticket Server

a. use centralized server to generate ID.  
b. but this will have single point of failure

## Snowflake approach

a. all above approaches have issues.  
b. snowflake = 1 bit reversed + 41 bits timestamp + 5 bits datacenter ID + 5 bits machine ID + 12 bits sequence number.  
c. sequence number is reset to 0 every millisecond, which means each machine can support 2^12 = 4096 new IDs per millisecond.  
d. 41 bits timestamp = 2^31 - 1 = 2199023255551 ms ~= 69 years
e. better to mention how to do clock sync between servers, Network Timke Protocol is the most popular solution.  
f. can talk about section length tuning. e.g fewer sequence numbers but more timestamp means lower concurrency but longer application life time.  
g. system needs to be high available.  
