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
* then use aggregation to aggregate on an interval (depends on use case, it could be daily or weekly). (Spark?)
* then use algorithms wo convert aggregated data into a trie structure
* store the trie Data into DB (string, date string, frequency of that week). Option 1: Document store like mongoDB, because we can periodically store a snapshot of serialized data, and mongoDB is a good fit fot serialized data. Option 2: Key-value store, where key is the prefix string and value is the top K results
