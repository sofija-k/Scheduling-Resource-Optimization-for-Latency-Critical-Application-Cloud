#!/bin/sh

MEMCACHE_SERVER_NAME="mvf0"


gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@memcache-server-$MEMCACHE_SERVER_NAME --zone europe-west3-a --command="
sudo apt update &&
sudo apt install -y memcached libmemcached-tools &&
sudo systemctl status memcached

"

# open memcached config file: sudo vim /etc/memcached.conf
# update memory limit: look for the line starting with -m and update the value to 1024
# expose the memcached server to external request: line starting with -l, replace localhost address with  internal IP of the memcache-server VM
# we can specify number of threads by introducing a line starting with -t followed by number of threads

# restart memcached: sudo systemctl restart memcached
