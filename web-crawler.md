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
* URL Frontier: stores URLs to be downloaded
* DNS Resolver: resolve url to ip address
* Content Parser: parse and validate content, could be async to gain more performance, so we make it a separate component
* Content Seen: compare the hash of the two web pages is much better to compare character by character
* Content Storage: Most of the content is stored on disk, popular content is kept in memory to reduce latency
* URL Filter: excludes certain content types, file extensions, error links and URLs in blacklisted sites
* URL Seen: Bloom filter or hash table
