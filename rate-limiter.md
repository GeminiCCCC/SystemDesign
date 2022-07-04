# algorithms

## 1. token bucket
a. bucket size and refill rate.   
b. each request consumer one token, if no token left request will be dropped.  
c. different bucket for different api.  


pros:
* easy to implement. 
* memory efficient. 
* allow a short period time of burst

cons:
* hard to tune

## 2. leaking bucket
a. bucket size and outflow rate.  
b. if bucket is not empty, request will be added to bucket, otherwise request will be dropped.  
c. outflow rate is fixed. 

pros:
* memory efficient give fixed bucket size
* request processing rate is stable

cons:
* cannot support burst traffic
* hard to tune given there are 2 parameters

## 3. fixed window

pros:
* memoery efficient
* easy to understand
* reset available quota at the end of time window fits certain cases

cons:
* burst traffic at edges of time windows could cause more traffic than allowed quota

## 4. sliding window log
a. store each request timestamp in redis as sorted set.  
b. when a new request comes in, remove all outdated timestamp who are older than the start of the current window, then add new request time window.  
c. if log size <= allowed count, accept the request, otherwise reject it

pros:
* very accurate

cons:
* use lot of memoery since even a request is rejected, its timestamp might still be stored in memoery

## 5. sliding window counter
a. current window request + previous window requests * percentage of overlap between sliding window and previous window, e.g. previous window has 5, current window has 3, and overlap is 70%. 3 + 5 * 0.7 = 6.5 < 7, so the request will be accepted

pros:
* smooths out spike traffic because it is based on average rate of previous window
* memoery efficient since we use counter

cons:
* assume previous window requests are evenly distributed, calculation is not 100% accurate. But according to experiments only 0.003% of requests are wrongly allowed

# Rate limiting rules

can use yaml config file to store

# Design details

a. when a request is rate limited, api returns http code 429 (too many requests).  
b. depending on the use cases, we may enqueue the requests to be processed layer. e.g order creations.  
c. client can get remaining number of allowed requests, limit threshold from the response header

# Race condition

Locks are obvious solution but will significantly slow down the system. Use Lua script and sorted sets data structure in Redis

# Synchronization issue

a. use sticky sessions that allow a client to send traffic to the same rate limiter. But it is neigher scalable nor flexible.  
b. a better approach is to use centralized data stores like Redis

# Performance optimization

a. use multi-data center to route use requests to the closest data center to reduce latency.  
b. sync data with evnetual consistency nodel.  

# Monitoring

make sure algorithm and rules are effective, depending on the monitor result adjust algorithm  

# Others

a. Hard vs soft rate limiting - requests can exceed the threshold for a short period.  
b. rate limiting at different levels.  
c. how how to avoid getting rate limited: use client cache, do not send too many requests in a short time frame, catch exceptions so your client can gracefully recover  
d. sufficient back off time to retry logic
