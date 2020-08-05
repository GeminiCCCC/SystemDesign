**1. if have static content such as HTML/CSS/JS, photos, and videos etc.. store them in a seperate NoSQL database. And use CDN (Content Delivery Network) to deliver to clients. The site's DNS resolution will tell clients which server to contact.**

Benefits:

  a. clients get content from server close to them
  
  b. your server does not need to serve the traffic for the content

**2. if you have web server, you can move the session related data into cache (Redis) to allow autoscaling (when creating new node, no need to copy session data from original node, can simply create all new nodes at the same time)**

**3. use master slave to reduce load from write master, only write to master and only read from slave**
