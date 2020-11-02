## 1. MD5

a - use md5 (message digest) to encrypt password or check if file had been modified during transfer, single bit change will result to completely different md5 value  
b - there are some websites can crack the MD5, they just brutal force pre calculated lots of MD5 values, so we can't directly store MD5 value as password, so we add salt (random value) to MD5, which meanss when storing password to the table we also need to store salt value so that later we can use the same salt value to verify the password. And a better way is to store the salt value itself to the encoded string to avoid creating new field in table.
