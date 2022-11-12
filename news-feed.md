## publish and retrieve feed api should take in auth_token as parameter

## separate post service, fanout service and notification service for a publish feed request
* use gateway/web server for authentication and rate limiting control

## fanout service
* push mode: friends news feeds get updated immediately, friends fetch feed will be fast. But for celebrity push mode will be slow, and fanout to inactive users will be a waste
* pull mode: fetching feed will be slow as it's on-demond
* we use hybrid mode: if user is not celebrity (flag stored in user table) use push mode, and when a user pulles his news feed, only use pull mode for celebrity friends.
* when pushing news to friends, first retrive friend lists, then filter out the friends who muted you, or you selectively do not want to share your news. Then send friends ID and new post ID (already persisted in database) to kafka queue
* kakfa queue consumers will write postID, friendID to the table (redis? mysql?)

## use CDN to retrieve static media data (image, video etc)

## cache is important for news feed system, 5 layers cache
* News feed: stores IDs for a feed
* Content: stores all post, popular post is stored in hot cache. others in normal cache
* Social graph: stores user relation data
* Action: likes a post or took other actions on a post
* Counters: like, reply, followers, following, etc
