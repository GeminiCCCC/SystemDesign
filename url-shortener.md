## back of the envelop estimation
* 100 mils URLS are generated per day
* write RPS = 100 mils / 24 / 3600 = 100 mils / 86400 ~= 100 mils / 100k = 1k
* assuming read/write ration is 10:1, read QPS = 10k
* assuming service runs for 10 years, average url length is 100 bytes, 365 * 100 mils * 10 years * 100 bytes = 365 bils * 100 bytes = 36.5 TB
