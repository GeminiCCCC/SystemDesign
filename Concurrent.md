## 1. Optimistic Lock and Pessimistic Lock:
Pessimistic lock is just select * from A for update, which assuming bad thing will happen and lock the record first  
Optimistic lock does not lock the record, instead when updating the record (select count with version first) it will check if version matches the current row version: update A set count = count-1 and version=version+1 where product_id=xxx and count>0 and version=<selected version>, and if update failed, it will select count with version again and then try to update again.
  
Cons:  
Pessimistic lock: all other threads will wait for one update to finish, if that update takes long time, all the threads allowed for mySQL will be used up and no more request can come in  
Optimistic lock: if there is a huge number of collision, e.g Amazon prime day deal. Do not use optimistic lock because some updates may alwaws fail since the backend version keep changing several times per second

Conclusion, use Pessimistic lock if there are manuy collisions and use Optimistic when there are less collisions

## 2. Use redis to handle requests, mySQL can only handle 1k concurrent sessions, redis can handle 100k concurrent sessions  
for amazon prime day case, store product_stock (e.g 10) to redis, then let application route the request to redis instead of mysql

## 3. how to make sure two DBs data are in sync when needs to update two DBs in different locations?   
  a - use Distributed Transaction: use Transaction Coordinator, if any write failed, notify all the other actions to do rallback  
  b - use Message Queue: if update to a DB failed, we can use MQ to repeatly process the event until it succeeded. 
  
## 4. use Circuit breaker (for controlling the load pression for the entire system), just add annotation on the service will a callback method and threshold, and when reaching the threshold, the call back method will respond error page.

## 5. use Rate Limiter (for controlling the access for one user)

## 6. before the peak event happens, downgrade unnecessary services, like comments, history data etc...  by returning some pre-defined data directly w/o querying backend DB

## 7. windows by ddefault provide port 1024-5000 to TCP/IP and will recycle them after 4 minutes, if there are many concurrent connection, it will used up all ports, then request will fail, to fix this. go to regedit, add MaxUserPort=65534 and TCPTimedWaitDelay=30 to HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters

## 8. when improving performance, 1. check if it's CPU intensive or IO intensive, CPU intensive means lots of calculation, sorting. IO intensive means intenet transfer, disk IO, memory IO (redis), SQL IO. To improve CPU performance, add more servers (more CPU). To improve IO performance, add hard drive add more memory, upgrade network card
