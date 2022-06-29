# algorithms #

## 1. token bucket ##
a. bucket size and refill rate.   
b. each request consumer one token, if no token left request will be dropped.  
c. different bucket for different api.  


pros:
* easy to implement. 
* memory efficient. 
* allow a short period time of burst

cons:
* hard to tune

## 2. leaking bucket ##
a. bucket size and outflow rate.  
b. if bucket is not empty, request will be added to bucket, otherwise request will be dropped.  
c. outflow rate is fixed. 

pros:
* memory efficient give fixed bucket size
* request processing rate is stable

cons:
* cannot support burst traffic
* hard to tune given there are 2 parameters

## 3. fixed window ##

pros:
* memoery efficient
* easy to understand
* reset available quota at the end of time window fits certain cases

cons:
* burst traffic at edges of time windows could cause more traffic than allowed quota

## 4. sliding window log ##
a. store each request timestamp in redis as sorted set.  
b. when a new request comes in, remove all outdated timestamp who are older than the start of the current window, then add new request time window.  
c. if log size <= allowed count, accept the request, otherwise reject it

pros:
* very accurate

cons:
* use lot of memoery since even a request is rejected, its timestamp might still be stored in memoery

## 5. sliding window counter ##
a. current window request + previous window requests * percentage of overlap between sliding window and previous window, e.g. previous window has 5, current window has 3, and overlap is 70%. 3 + 5 * 0.7 = 6.5 < 7, so the request will be accepted

pros:
* smooths out spike traffic because it is based on average rate of previous window
* memoery efficient since we use counter

cons:
* assume previous window requests are evenly distributed, calculation is not 100% accurate. But according to experiments only 0.003% of requests are wrongly allowed
