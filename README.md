**1. if have static content such as HTML/CSS/JS, photos, and videos etc.. store them in a seperate NoSQL database. And use CDN (Content Delivery Network) to deliver to clients. The site's DNS resolution will tell clients which server to contact.**

1.1 Benefits:

  a. clients get content from server close to them
  
  b. your server does not need to serve the traffic for the content

1.2 CDN is another type of cache

1.3 if the system is not large enough to have its own CDN, we can use lightweight web server like Nginx, and cutover the DNS from our servers to a CDN later

**2. if you have web server, you can move the session related data into cache (Redis) to allow autoscaling (when creating new node, no need to copy session data from original node, can simply create all new nodes at the same time)**

**3. use master slave to reduce load from write master, only write to master and only read from slave**

**4. can also add load balancers in front of read replicas**

**5. CAP**

CA - RDBMS, Neo4J(graph)

AP - Riak(KV), Couchbase(Document Stores), Cassandra(Column Oriented)

CP - Redis(KV), MongoDB(Document Stores), HBase(Column Oriented)

**6. Redis vs Memcached**

a. Redis supports server-end data operations and owns more data structures and supports richer data operations. For complicated data operation Memcached will needs to copy data to client side and then set the data back which will greately increase the IO counts. So if you need cache to support more complicated structures and operations, Redis is a good choise. Memcached only supports simple K-V structure while Redis supports String, Hash, List and Sorted Set

b. Redis only uses single core whilc Memchased utilizes multiple cores. So Redis will perform better with small data storage. Memcaches outperforms Redis for storing data of 100k or above

c. Memcached all data storage occurs in memory while for Redis when the phiscal memory is full Redis swap values not used for a long time to the disk.

d. Redis support data persistence: RDB snapshot and AOF log, while Memcached does not support data persistence operations.

e. Memcached itself does not support distributed mode, You can only achieve it on the client side through distributed algorithms such as Consistent Hashing. While Redis Cluster supports the distrbuted mode from server side
