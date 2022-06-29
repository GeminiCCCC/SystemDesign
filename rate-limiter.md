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
