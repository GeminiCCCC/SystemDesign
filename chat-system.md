## clarify the type of chat app
* 1 to 1 like Facebook messenger, whatsapp, wechat
* group chat like slack
* game chat like discord who focus on large group interaction and low voice chat latency

## clarify the scope
* is it a mobile app or web app? both
* DAU: 50 mils
* max group chat people limit: 100
* what feature do we need to support? 1 on 1, group chat, online indicator, only text message, no attachment support
* is there a message size limit? yes, 100,000 characters long
* is end-to-end encryption required? not now
* how long will the chat history store? forever
* do we need to support message sent and read feature? maybe

## protocol
* UDP: User datagram protocal, faster, no order and deliveribility guarentee, good for voice service
* TCP: Transimission control protocal, slower, more reliable, the order of packet sent can be guarenteed
* poll: client periodically ask server if I have new msg, this will cause server waste resources to answer requests that have no data returned
* long polling: client holds the connection open until there are actually new msgs available or a timeout threshold has been reached. Once the client receives the msg, the current connection will be closed and a new long polling connection request. The issues are: 1. sender and receiver may not connect to the same server, HTTP based servers are usually stateless, the server receives the msg may not have the long polling connection with the client who sends sthe msg. 2. server has no good way to tell if a client is closed. 3. it is inefficient. If a user does not chat much, long polling still makes periodic connestions after timeout
* WebRTC: web real-time communication, an open-source, browser-standardized framework that allows you to engage in rich, multimedia communication in real time. It's built right into most browsers and uses APIs to establish a peer-to-peer connection, so no need to download third-party plugins. There are also WebRTC SDKs targeting different platforms, such as iOS or Android.  
  **Pros**:  
  * provide strong security guarentees; data is encrypted and authenticated with SRTP (Secure Real-Time Transport Protocal). 
  * open-source and free to use, backed by a strong and active community
  * platform and device-independent. Will work on any browser that supports it, irrespective of OS or the types of devices.  
 **Cons**:
  * even though it is a peer-to-peer technology, you still have to manage and pay for web servers
  * can be extremely CPU-intensive, especially when dealing with video content and large groups of users. This makes it costly and hard to reiably use and scale WebRTC applications
  * hard to get started with. Ramp up path is steep, plenty of concetps you need to explre and master: the various WebRTC interfaces, codec & media processing, network address translations (NATs) & firewalls, UDP, and many more

* WebSocket: a realtime technology that enables full-duplex, bi-directional communication between a web client and a web server over a persist, single-socket connection. It starts as an HTTP req/resp handshake. If the handshake is successful, the client and server have agreed to use the existing TCP connection as a WebSocket connection. This connection is kept alove as long as needed.  
  **Pros**:
  * comparing to long polling, it eliminates the need for a new connection with every request, drastically reducing the size of each msg (no HTTP headers)
  * As an event-driven technology, it allows data to be transfereed without the client requesting it (server side event).  
  **Cons**:
  * stafeful, ticky to handle, especially at scale, becuase it requires the server layer to keep track of each individual WebSocket connection and maintain state info
  * don't automatically recover when connections are terminated, you need to implement yourself
  * certain enviroments (such as corporate networks with proxy servers) will block WebSocket connection
* WebRTC vs WebSockets:
  * WebSocket provides a client-server computer communication protocal, where as WebRTC offers a peer-to-peer protocal and communication capabilities for browsers and mobile apps
  * WebSocket works over TCP, WebRTC is primarily uses over UDP (although it can work over TCP as well)
  * WebRTC is primarily designed for streaming audio and video contents. It is possible to stream media with WebSockets too, but the WebSocket is better suited for transmitting text data
* XMPP vs WebSocket
  * XMPP has better security comparing to WebSocket
  * XMPP is decentralized, while WebSockets follows a centralized architechture. XMPP is based on the client-server model and prevents direct interaction between clients. WebSockets take the help of APIs and ensure the client and server are communicating continuously.
  * For speed, WebSocket outperforms XMPP because of its centralized nature and continual communications. XMPP force authentication and authorization of both the server and the client slows down its performance a bit.
  * Use WebSocket is speed is more important, use XMPP if security is more important
## stateless services
* discovery service: 
  * recommend the best chat server for a client based on the criteria like geographical location, server capacity etc. 
  * use zoo keeper, it registers all the available chat servers and picks the best chat server
  * User tries to log in to the app -> The LB sends the login request to API servers -> after the backend authenticates the user, service discovery finds the best chat server -> User connects to selected chat server through WebSocket
![image](https://user-images.githubusercontent.com/68412871/201559921-a624737e-695b-42cf-aab9-780ce505a85f.png)
* presence service (manage online/offine status)
  * create table to store user info including online status
  * when user logged in and the WebSocket connection is established, mark status to true. 
  * when user logged out, mark status to false
  * when user logged in, he gets his friends list first. Then query cache for friends online status, if not found, query DB
* sign up, user profile, authentication service
## stateful service
* chat service:
## third party integration
* push notification: inform users when new msgs have arrived
## Scalibility
* with 1M concurrent users, assume 1 connection needs 10K memory, only needs 10G memory, so one server can handle all connections
## high level
* User makes http call to LB to API servers which include signup, login, change profile etc
* User makes websocket call to chat service
* Chat service facilitates msg sending/receiving
## storage
* for user profile, user setting, user friends, we use relational DB
* for chat history, previous study reveals that Facebook messenger and Whatsapp processes 60 bils msgs a day. Only recent msgs are accessed frequently. But user might still require random access of data, such as search, view your mentions, jump to a specific msg etc. read/write rations is about 1:1
* select key-value store for chat history. HBase and Cassandra are column oriented, but stores in key-value pairs. Because it can scale horizontally easily; provides very low latency to access data; Relational DBs do not handle long tail of data well, when indexes grow large, random access is expensive
## Data model
* 1 on 1 chat: msg_id bigint, msg_from bigint, msg_to bigint, content text, created_at timestamp
* group chat: group_id bigint, msg_id bigint, user_id bigint, context text, created_at timestamp
## msg_id
* msg_id should be unique and sortable, because multiple msg could happend within same timestamp
* first option is auto increment field, but nosql DB usually does not support it
* second option is use global 64-bit sequence number generator like Snowflake
* third option is to use local sequence number generator, this is works because the msg_id only needs to be unique within 1 to 1, or group chat
## msg flow
![image](https://user-images.githubusercontent.com/68412871/201560089-b25664c3-c567-4b5b-9632-3f9037671723.png)
  1. User A sends a chat message to Chat server 1 (server was assigned by discovery service while logging in)
  2. Chat server 1 obtains a message ID from ID generator
  3. Chat server 1 sends the msg to the msg sync queue
  4. The msg is stored in a key-value store, after this we can send back ack to client to mart msg as sent on the client side
  4.1 Here there should be another user mapping service, every time when a user log in, it will maintain the userId and the websocket connection ID. And it will find user B's websocket connection 
  6. a. if user B is online, the msg is forwarded to Chat server 2 where User B is connected. b. if B is offline, a push notification is sent from PN service
  7. Chat server 2 forwards to msg to User B.
## multiple device sync
* each client keeps cur_max_msgID
* when new client connects, if will query key-value store and query some recent msgs by filtering the msg_to and compare the msg_id
## group chat
* we can create groupChat table to store user and group mapping
* when a msg is sent, we can copy the msg to all group member's msg queue (by querying the groupChat table), pros is client only needs to check its own queue. cons is if group is too big, this fanout behavior will be expensive. So for a large group we can publish the msg to a shared queue, and all users will subscribe from the queue
## user disconnection
* disconnection can happen due to either user manually close the chat screen, or the internet is not stable or lost
* naive approach is that every time the connection is lost/established, we update the status. But this will maker the presence indicator change too often, and resulting in poor user experience.
* we can use heartbeat, client send hearbeat to server every 5 seconds, if no heartbeat after 30s, mark user to be offline. If user was offline and the heartbeat comes, mark the user to be online.
## online status fanout
* pull mode: interval 1 min, has delay, most requests don't have any meaning
* push mode: real-time, but fanout number could be big
* for friends status update, we use push mode to notify all online friends I am online (since online friends are limited)
* for group status update, we use pull mode (e.g. user joins 20 groups, each group has 200 people, 20% members are online, thats 20*200*0.2=800 events), we can pull the group members status when first entering the group. After that user can manually update members status

## cache
* when user set online/offline status, we can add to cache cluster before database, so that when read we check cache first to reduce the load on DB read











