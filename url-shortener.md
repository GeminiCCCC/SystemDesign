## back of the envelop estimation
* 100 mils URLS are generated per day
* write RPS = 100 mils / 24 / 3600 = 100 mils / 86400 ~= 100 mils / 100k = 1k
* assuming read/write ration is 10:1, read QPS = 10k
* assuming service runs for 10 years, average url length is 100 bytes, 365 * 100 mils * 10 years * 100 bytes = 365 bils * 100 bytes = 36.5 TB

## API
* POST api/v1/data/shorten: param = longURL, return = shortURL
* URL redirecting GET api/v1/shortUrl: return = longURL

## URL redirecting
* server returns longUrl along with code 301 (redirect)
* 301 vs 302: 301 means short url is permernently moved to long url, and the long url will be cached in browser, and subsequent requests will not hit server. 302 means temporarily moved to long url, so subsequent requests will hit server again. 301 can reduce server load, and 302 can help track the click count and request source, discuss pros and cons

## Storage
* could use hash table where the key is shortURL and value is longURL, but machine has memory limit, we can't store all urls into memory
* a better way is to store it in a relational DB
* character is [0-9], [a-z], [A-Z], which is 10 + 26 + 26 = 62, so we need enough chars to support 365 bils urls, 62^7 ~= 3.5 trillions, so 7 chars is enough

## Hashing
* CRC32 = 8 chars, MD5 = 32 chars, sha1 = 40 chars
* to make it shorter first approach is to use first 7 chars, but this will lead to hashing collision, one way to solve it is that once we found the hashed value exists in DB, we append a predefined string to the longURL until no collision was found. However query DB is expensive, a bloom filter can can improve performance
* a better appraoch is use base 62 conversion which keeps dividing 62 and use the reminder. A few differences: a. length is not fixed b. we need a unique ID generator (base 10 ID) c. no collision because ID is unique d. can guess next hash value if ID is increased by 1, might be a security issue

## Flow
* longURL comes in -> check if it exists in DB, if yes return shortURL -> generate new ID -> hash to short URL -> save ID, short and long URL in DB
* for url redirect use cache, request will be routed by load balancer to web server who will query distributed cache first, it miss, query DB if found, update cache
