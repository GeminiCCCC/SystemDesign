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
* not easy to tune

## 2. leaking bucket ##
