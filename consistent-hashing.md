## 1. map key to ring and search for server clockwise

## 2. physical server on the ring has issue that if a server is added or removed, keys for each server are not evenly distributed

## 3. use virtual nodes (hundreds) for each server to solve it, tradeoff is that more spaces are needed to store data about virtual nodes. And we can tune the number of virtual nodes

## 4. when a new server is added, move anticlockwise until a server is found, thus all keys have found should be mapped to new server
