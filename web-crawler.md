## Ask clarification questions
* use case  
  a. Search engine indexing.  
  b. Web archiving: e.g. national libraries run cralwers to archive web sites.  
  c. Web mining: e.g. financial firms use crawlers to download shareholder meetings and annual reports to learn key compan initiatives.  
  d. Web monitoring: e.g. monitor copyright and trademark infringements over the internet.  
* Ask total web pages to collect per month: e.g. 1 billion pages
* Ask what content types are included: e.g. HTML only or PDFS ans images as well
* Ask how long do we need to store the content
* Ask how to handle duplicated content in pages

## Non functional requirements
* Scalability: need to be able to run in parallel
* Robustness: need to handle bad html, unresponsive servers, crashes, malicious links etc
* Politeness: should not make too many requests to a website within a short time interval
* Extensibility: minimal changes are needed to support new content types

## Back of the envelope calculation
* QPS: 1,000,000,000 / 30 days / 86,400 seconds = 1,000,000,000 / 2,592,000 = ~400 pages per second
* Peak QPS = 2 * 400 = 800
* Assume average page size is 500k
* 1 billions pages * 500K = 1 GB * 1,000 * 500 = 500 TB
* 500 TB * 12 months * 5 years = 30 PB

## High level
![image](https://user-images.githubusercontent.com/68412871/193431435-c5527345-15b0-4fee-859b-6f679f091954.png)

* Seed URLs: based on locality as different countries may have different popular websites. Or based on topics, for example shopping, sports, healthcare etc
* URL Frontier:   
![image](https://user-images.githubusercontent.com/68412871/193436707-9381a360-afed-41ea-a3bf-14a6e23ef78c.png)

  1. stores URLs to be downloaded. Since it can be hundreds of millions or urls, we can't store all in memory, not enough space and not durable. And we can't store all in disk because it's too slow. We can use hybrid approach, which is Kafka queues which support both in memory and disk storage to maintain all the URLs that need to be crawled.
  2. maintain domain to queue mapping, all domain's urls are stored in the same queue
  3. a worker thread download page from queue one by one with delay in between
  4. a prioritizer to calculate page priority and publish into different priority queue and a queue selector will use probablity to select from priority queues
  5. to keep data refresh we need to do recrawl in Frontier with an internal cron worker. Recrawl all the URLs is time-consuming and resource intensive. We can recrawl base on webpage update history, and recrawl high priority pages more frequently
  6. partition urls and distribute them to HTML Downloader
* HTML Downloader:
  1. Read each website Robots.txt for allowed pages
  2. Cache the result to memory for performance improvement
  3. Multiple servers with multiple threads on each server
  4. Send urls to the HTML Downloader which are geographically closer to the website servers
  5. Apply timeout for downloading pages, incase some web servers have slow response time to increase performance
* DNS Resolver: resolve url to ip address
  1. DNS response time ranges from 10ms to 200ms
  2. call to DNS Resolver is synchronus call due to the nature of many DNS interfaces
  3. cache DNS result and use cron job to preodically update it
* Content Parser: parse and validate content, could be async to gain more performance, so we make it a separate component
* Content Seen: compare the hash of the two web pages is much better to compare character by character
* Content Storage: Most of the content is stored on disk, popular content is kept in memory to reduce latency
* URL Filter: excludes certain content types, file extensions, error links and URLs in blacklisted sites
* URL Seen: Bloom filter or hash table

## DFS vs BFS
* DFS is not a good choice because the depth of DFS can be very deep
* BFS is commonly used by web crawlers, but it as two problems (refer URL Frontier section for solution):
  1. Most links from the same web page are linked back to the same host (domain). When the crawler tries to download wbe pages in parallel, target site server will be flooded which is considered as "impolite"
  2. Standard BFS has no priority for a URL as not every page has the same level of quality and importance

## Robustness
* Consistent hashing to evenly distribute urls to downloaders. Safely and efficiently add or remove a downloader server
* Store crawler state and data, so in the casue of failure a distributed cralwer can load the data and restart easily
* Handle errors gracefully without crashing the system
* Data validation

## Extensibility
![image](https://user-images.githubusercontent.com/68412871/193469782-31451028-da5d-47ab-92a3-830e705aa37c.png)
