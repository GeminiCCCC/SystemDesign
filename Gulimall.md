## 1. OAuth2.0

a. 3rd party sites ask user to verify with QQ Authorization Server  
b. QQ Authroization Server returns the code
c. 3rd party sites use code to ask QQ Authorization Sever for Access Token (code can only be used once)
c. 3rd party sites use Access Token to ask QQ Resource Server for user's open information e.g. profile, avatar, nickname etc... (Access Token has expiration time)

## 2. Offline cart data storage options:

a. localstorage (stores in user's browser)/cookie/WebSQL, pros: release backend pressre. cons: backend server does not have the data and cannot use the data to do recommendation service based on the items in the offline cart  
b. redis is a better option since redis has hight throughput and can also persist data

## 3. Idempotency

a. Idempotent: select, insert with primary key, update to a specific value  
b. Not idempotent: increase qty

solution:

 1 - token: before sending business request, get token and store it to Redis in server. add token to the request and on the server side check if token exists in redis, if it exists then execute and delete token. If not exists, means duplicate requests, just ingore it
