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
  * platform and device-independent. Will work on any browser that supports it, irrespective of OS or the types of devices


* WebSocket: a realtime technology that enables full-duplex, bi-directional communication between a web client and a web server over a persist, single-socket connection. It starts as an HTTP req/resp handshake. If the handshake is successful, the client and server have agreed to use the existing TCP connection as a WebSocket connection. This connection is kept alove as long as needed.
