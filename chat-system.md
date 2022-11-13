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
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
