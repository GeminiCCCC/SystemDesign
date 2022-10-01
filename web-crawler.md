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
* 1 billions = 1
