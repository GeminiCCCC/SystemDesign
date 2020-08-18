**1. if have static content such as HTML/CSS/JS, photos, and videos etc.. store them in a seperate NoSQL database. And use CDN (Content Delivery Network) to deliver to clients. The site's DNS resolution will tell clients which server to contact.**

1.1 Benefits:

  a. clients get content from server close to them
  
  b. your server does not need to serve the traffic for the content

1.2 CDN is another type of cache

1.3 if the system is not large enough to have its own CDN, we can use lightweight web server like Nginx, and cutover the DNS from our servers to a CDN later

**2. if you have web server, you can move the session related data into cache (Redis) to allow autoscaling (when creating new node, no need to copy session data from original node, can simply create all new nodes at the same time)**

**3. use master slave to reduce load from write master, only write to master and only read from slave (MongoDB)**

**4. can also add load balancers in front of read replicas**

**5. CAP**

CA - RDBMS, Neo4J(graph)

AP - Riak(KV), Couchbase(Document Stores), Cassandra(Column Oriented)

CP - Redis(KV), MongoDB(Document Stores), HBase(Column Oriented)

**KV**: Simple schema; High velocity read/write with no frequent updates; High performance and scalability; No complex queries involving multipl key or joins

**Document Stores**: Flexible schema with complex queryihng; JSON/BSON or XML data formats; Leverage complex Indexes(multikey, geospatial, full text search etc); High performance and balanced R:W ratio; if each record is not that big and has limited size (e.g not more than 1MB, then probably we don't need to use Document  stores)

**Column Oriented**: High volumn of data; Extreme write speeds with relatively less velocity or reads; Data extractions by columns using row keys; No ad-hoc query patterns, complex indices or high level of aggregation. Good for time-series data.

**Graph Stores**: If you need relationships between record, use graph stores

**Cassandra:**

a. no master-slave, instead peer-to-peer (protocal "gossip")

b. high availability and tunable consistency (since A and C are opposite, in order to get C you have to wait until all nodes are consistent which will decrease A), conflicts are solved during reads as focus lies on write-performance

c. Data is stored in sparse multidimensional hash tables, each row has unique key(used by partitioning), and each row has non-fixed number of sorted key/value pairs(each pair is a column). Map(RowKey, SortedMap<ColumnKey, ColumnValue>> (RowKey should be hashed, in order to distribute data across the cluster evenly)

d. Optimized for writing, but fast read are possible as well

e. has no aggregation framework and requires external tools like Hadoop, Spark and others

f. is a much more stationary database. It facilitates static typing and demands categorization and definition of columns beforehand.

g. only has cursor support for the secondary index. Its queries are limited to single columns and equality comparisions.

**MongoDB:**

a. JSON style document store, and can support richer data model than Cassandra

b. single master directing multiple slaves, if master node goes down, it make take up to 1 minute to elect a slave node to become the master. And during this time there is no availability

c. has built-in aggregation framework, but is only efficient when working with small or medium-sized data traffic

d. does not require a schema, natually making it more adaptable to change

e. has high-quality second indexes

f. Each record will have a UUID (unique object Id) consists of 12 bytes: 4 bytes = Unix timstamp, 3 bytes = machine Id, 2 bytes = session Id, 3 bytes = seq. Cons of UUID is too long, takes too much space and searching is slow

**6. Redis vs Memcached**

a. Redis supports server-end data operations and owns more data structures and supports richer data operations. For complicated data operation Memcached will needs to copy data to client side and then set the data back which will greately increase the IO counts. So if you need cache to support more complicated structures and operations, Redis is a good choise. Memcached only supports simple K-V structure while Redis supports String, Hash, List and Sorted Set

b. Redis only uses single core whilc Memchased utilizes multiple cores. So Redis will perform better with small data storage. Memcaches outperforms Redis for storing data of 100k or above

c. Memcached all data storage occurs in memory while for Redis when the phiscal memory is full Redis swap values not used for a long time to the disk.

d. Redis support data persistence: RDB snapshot and AOF log, while Memcached does not support data persistence operations.

e. Memcached itself does not support distributed mode, You can only achieve it on the client side through distributed algorithms such as Consistent Hashing. While Redis Cluster supports the distrbuted mode from server side

**7. Kafka**

a. pub/sub messaging rethought as a distributed commit log

b. consumer controls his own state, using an (offset, length) style API

c. Messages are persistent

d. after putting message into queue, how to get the result from the message? one way is after putting message into queue, producer will receive acknowledgement with message reference, and once the message is finished processing, the result will be stores in some places and producer will periodically use the acknowledgement to check if the message is finished or not.

**8. Load balancer and reverse proxy**

a. both have SSL termination

b. LB has session persistence

c. reverse proxy has compression, caching etc..

d. use LB if you have multiple servers

e. solution such as NGINX and HAProxy can support both layer 7 LB and reverse proxying

f. reverse proxy is comparing with forward proxy, where forward proxy exists on the client side and reverse proxy exists on the server side

g. LB/reverse proxy secures the backend web servers from attack, as the only network connections they need to open are from the secure LB

**9. Design Messaging System**

a. use XMPP (extensible messaging presence protocal)

b. use session services to store which user is connecting to which gateway box, and then route the message to the correct gateway box

**10. Design youtube video view counts**

a. instead send each click to the database directly, send the count to the Kafka queue and processing service will consume the event and aggregate the count in in-memory counter. And flush the counter data to database every few seconds

b. we can also add API gateway between client and LB, and the API gateway can batch the request and send the data in one reqeust to LB

c. data roll up, after a while roll up data per minute to per hour, and more time later, roll up data per hour to per day. And move cold data to object store

d. if processing service cannot keep up with the load, for example because of a super hot video. what can you do? we can batch the event data into an object store, such as S3 and then send a message to the message broker, then we will have a big cluster of machines to retrieve the messages from the message queue, read the data from S3 and process them. This approach is a bit slower than stream processing, but faster than batch processing

**11. if the data is too much to be stored in the cache, we can dump the data to the disk and then use MapReduce service to aggregate the data from disk**

**12. better serialize data into binary format to save network IO (Apache Avro)**

**13. when designing data streaming system, we will need to keep reducing the request rate. From billions of requests from each client, then we pre_aggregate data on each API gateway host for several seconds and then go to Kafka. And we can always parition data into different partitions and process each partition of data in parallel, and then aggregate data in memory**

**14. in queue each message is consumed by one consumer while in topic, each message goes to all the subscribers**

**15. how each host talks to other hosts?**

a. first approach is message broadcasting, tell everyone everything. This approach is easy to implement and works for small cluster but not scalable, as the hosts increased the messages need to be broadcasts will be increased quadratically.

b. second is gossip protocal, within a given frequcency, each machine picks another machine randomly and shares data (Yahoo use this)

c. thrid is to use distributed cache (Redis)

d. forth is coordination service (choose one host as a leader and other nodes only share data with leader), or a separate Zookeeper coordination service 

e. TCP vs UDP: TCP guarantees delivery of data and the packets will be delivered in the same order they were sent; UDP does not guarantee the order of the packets, but it's faster. So if we want more accurate with a bit performance overhead then TCP; otherwise UDP

**16. how to do retry?**

exponential backoff and jitter: every retry interval will increased exponentially and plus a random number to prevent many retries happen at the same time

**17. how host find which distributed cache node?**

a. ask centralized configuration service (e.g ZooKeeper) about which node to connect

b. ask any node (gossip protocal)

**18. how many QPS can different database handle?**

And this value comes from the CPU frequency

SQL - 1k/s

Cassandra - 10k/s 

**19. Long Polling vs WebSockets**

Long Polling: 

a. client sends an XMLHttpRequest/AJAX request - > server doesnot immediately respond but wait until there is new data available -> server responds with new data -> clients receives the data and initiate next request immediately

b. Message ordering and delivery not guarantee.

c. performance and scaling not good

d. server side load is heavy

WebSockets:

a. computer communication protocal which provides full-duplex communication channels over a single TCP connection (guarantee message ordering and delivery)

b. different from HTTP but compatible with HTTP
