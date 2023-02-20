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
