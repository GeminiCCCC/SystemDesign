## 1. OAuth2.0

a. 3rd party sites ask user to verify with QQ Authorization Server  
b. QQ Authroization Server returns the code  
c. 3rd party sites use code to ask QQ Authorization Sever for Access Token (code can only be used once)  
d. 3rd party sites use Access Token to ask QQ Resource Server for user's open information e.g. profile, avatar, nickname etc... (Access Token has expiration time)

## 2. Offline cart data storage options:

a. localstorage (stores in user's browser)/cookie/WebSQL, pros: release backend pressure. cons: backend server does not have the data and cannot use the data to do recommendation service based on the items in the offline cart  
b. redis is a better option since redis has high throughput and can also persist data

## 3. Idempotency

a. Idempotent: select, insert with primary key, update to a specific value  
b. Not idempotent: increase qty

solution:

 1 - token: before going to the submit order page, service will use store a token (key=ORDER_TOKEN_PREFIX+userId, value = UUID, expiry = 30 minutes) to Redis. same token will also be stored to the webpage in a hidden field, then user click submit order. add token to the request and on the server side check if token exists in redis, if it exists then execute and delete token. If not exists, means duplicate requests, just ingore it  
 2 - for data only want to be processed once, we can calculate its MD5 value and store it to Redis, it already exists then do not process it

## 4. Redis

a. use lua script to ensure atomicity, put the operations that need to have atomicty to lua script and let Redis execute it, and Redis will ensure the atomicity

## 5. Distributed transaction

a. SEATA has TM (Transaction manager), RM (Resource manager) and TC (Transaction controller), business start service will create TM and RM is configured on each service, TC is global controller. any service failed, TC will know which services need to roll back.  
b. SEATA AT mode how to roll back commited data, create undo_log in each service's database. It will record the original value before any change. When it needs to roll back it will just use the original value to update again  
c. but SEATA is not good for high concurrency since it will make many locks to do the global TC control, so to handle this issue we can use message queue to notify the remote service to roll back its committed operation

## 6. Message queue

a. to guarantee message delivery to MQ: 1) retry when failed. 2) log success or fail (create log table in DB), then periodically scan log table for failed logs and resend  
b. to handle double delivery: 1) make sure consumer's logic is idempotent (e.g always check status before update) 2) create log tables for each message in redis/mysql, always check if message has been processed before using it again, similar to the first solution 3) RabbitMQ has Redelivered status, but need to check if it's a valid redelivery or not  
c. how to handle too many messages stuck in the MQ: 1) limit pubisher sending rate 2) setup more consumers 3) use separate message service to quickly consume messages out of the MQ and store them into DB and then process them later so that we can improve the MQ performance

## 7. second kill

a. assign a random code (UUID) for each product for current second kill event, and store it to Redis, so that it can prevent attack because the request need both skuId and random code to communicate with server  
b. use product count as redis semaphore to only allow certain amount of requests to communicate with service, key is prefix + product random code (use random code to prevent url attack, incase someone knows the productId)
