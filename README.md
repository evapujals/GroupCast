# GoTorrentGossip
[![Code Health](https://landscape.io/github/evapujals/GoTorrentGossip/master/landscape.svg?style=flat)](https://landscape.io/github/evapujals/GoTorrentGossip/master)
[![Build Status](https://travis-ci.org/evapujals/GoTorrentGossip.svg?branch=master)](https://travis-ci.org/evapujals/GoTorrentGossip)

-----------------------------
###### Task #1: Asynchronous calls, gossip-based
dissemination, push-pull gossip
-------------------------------------
###### Tracker.py
**Actor tracker**
Tracker is responsible of membership management functions.
###### Peer.py
**Actor peer**
Peers use gossip to distribute the file chunks.
###### Impress.py
Impress has been implemented in order to avoid problems with printing using intervals.
###### Push.py
Peers ask for random pieces
###### Pull.py
Peers ask for the pieces that they need (missing pieces)