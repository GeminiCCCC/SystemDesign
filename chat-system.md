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
* poll: client periodically ask server if I have new msg, this will cause server waste resources to answer requests that have no data returned
* long polling: client holds the connection open until there are actually new msgs available or a timeout threshold has been reached. Once the client receives the msg, the current connection will be closed and a new long polling connection request. The issues are: 1. sender and receiver may not connect to the same server, HTTP based servers are usually stateless, the server receives the msg may not have the long polling connection with the client who sends sthe msg. 2. server has no good way to tell if a client is closed. 3. it is inefficient. If a user does not chat much, long polling still makes periodic connestions after timeout
