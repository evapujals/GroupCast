# GoTorrentGossip
[![Code Health](https://landscape.io/github/evapujals/GoTorrentGossip/master/landscape.svg?style=flat)](https://landscape.io/github/evapujals/GoTorrentGossip/master)
[![Build Status](https://travis-ci.org/evapujals/GoTorrentGossip.svg?branch=master)](https://travis-ci.org/evapujals/GoTorrentGossip)

-------------------------------------
###### Task #2: Lamport clocks, total ordering, failure tolerance, leader election
-------------------------------------
###### Group.py
**Tracker** is responsible of membership management functions.
The classical functionality: join, leave and get_members.
###### Peer.py
**Peer**--
Basic implementation to manage a member of a group.
**LamportPeer**--
Each message m is always timestamped with the current Lamport clock of its sender.
###### Sequencer.py
**Sequencer** is used to implement total ordering.
A sequencer is a process that assigns a unique timestamp seq to every message m that it receives, and multicasts it to every other member of the group.
A failure tolerance mechanism is provided in this part.
The bully leader election algorithm to elect a new sequencer when it fails is implemented.
###### Impress.py
**Impress** has been implemented in order to avoid problems with printing using intervals.
