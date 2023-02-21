# Scope and requirements
* Does the matching only support prefix match? yes
* How many suggestions should we return? 5. By what? popularity and query fruquency
* Spell check? No
* Search in english? yes. can talk multi language support if have time
* all lowercase? yes
* DAU? 10 millions
* response time should be within 100 ms
* results will be sorted by popularity
# Back of the envelope estimation
* average 10 searches per day per person
* 20 bytes per query string, each byte is a query
* 10 mil * 20 * 10 / 86400 = 2 bil / 86400 ~= 24K QPS
* peak QPS = 24k * 2 = 48K 
* assume 20% of daily queries are new, 10 mil * 20 * 10 * 0.2 = 0.4 GB
# Simple version
* create table with two fields, string and frequency
* when select * from table where string like 'prefix%' order by freqency desc limit 5
* this will only work with small data set
# Trie
* root node is empty
* each node has 26 children
* each node stores the whole string starting from root node
* frequency is stored inside the node
* first find the starting node by using the prefix, then traverse the sub tree to find all leaf nodes
![image](https://user-images.githubusercontent.com/68412871/220189888-aff342b7-ea79-45e6-8b49-831911239e2a.png)

# Optimization
* to get top k, worst case scenario is to traverse the entire tree
* step 1: limit k to like 50, since users won't type in a long word
* step 2: cache top k at each node
* we trade more space with less time which is a good deal
# Data gathering service
* not real-time
* from analytics logs (e.g. words and datetime), no index
* for a large scale system, logging each log may be too much, we can also sample the logs
* then use aggregation to aggregate on an interval (depends on use case, it could be daily or weekly). (Spark?)
* then use algorithms wo convert aggregated data into a trie structure
* store the trie Data into DB (string, date string, frequency of that week). 
  * Option 1: Document store like mongoDB, because we can periodically store a snapshot of serialized data, and mongoDB is a good fit fot serialized data. 
  * Option 2: Key-value store, where key is the prefix string and value is the top K results
* also store result in cache weekly
# Query service
* query gets sent to LB
* LB routes the requests to API servers
* query redis cache first
* if cache missed, query trie DB
* result can also be stored in broswer cache to improve response time
# Trie operations
* Create: weekly from aggregated logs
* Update: 
  * option 1: regenrate weekly
  * option 2: if trie is small, update individual node is also acceptable. All its parent nodes will be updated
  ![image](https://user-images.githubusercontent.com/68412871/220191208-d8117c36-9f30-4dda-8805-95daffd2deb1.png)
* Delete: We need to remove hateful, violent, sexually explicit or dangeroud autocomplet suggestions. We can add a filter layer between API servers and cache. And asynchronosly remove actuall data from trie DB
# Scale the storage
* when the data cannot be stored in one server, we need to shard the data. 
* naive approach is shard by english letter, but that will only give us 26 partitions and could result to hot partitions
* to partition more, we can shard on second or even third letters e.g aa - ag
* an improvement is to maintain a lookup with key is partition key and value is the records for the key, and group smaller group together
* or we could hash the key and partition the hash to have better even distribution
# Follow up
* multi language support: store unicode characters in trie nodes
* how to support realtime treading events: data comes as streaming, use Spark and Kafka etc.
