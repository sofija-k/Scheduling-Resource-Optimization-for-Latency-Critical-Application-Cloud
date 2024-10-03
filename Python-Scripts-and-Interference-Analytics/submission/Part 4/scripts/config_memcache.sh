#!/bin/sh

MEMCACHE_SERVER_NAME="pn2l"


gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@memcache-server-$MEMCACHE_SERVER_NAME --zone europe-west3-a --command="
sudo apt update &&
sudo apt install -y memcached libmemcached-tools &&
sudo systemctl status memcached &&
sudo apt install -y python3 python3-pip &&
pip3 install psutil docker &&
sudo usermod -aG docker \$USER &&
newgrp docker
"

gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@memcache-server-$MEMCACHE_SERVER_NAME --zone europe-west3-a --command="
docker pull anakli/cca:parsec_blackscholes &&
docker pull anakli/cca:parsec_canneal &&
docker pull anakli/cca:parsec_dedup &&
docker pull anakli/cca:parsec_ferret &&
docker pull anakli/cca:parsec_freqmine &&
docker pull anakli/cca:splash2x_radix &&
docker pull anakli/cca:parsec_vips
"

# open memcached config file: sudo vim /etc/memcached.conf
# update memory limit: look for the line starting with -m and update the value to 1024
# expose the memcached server to external request: line starting with -l, replace localhost address with  internal IP of the memcache-server VM
# we can specify number of threads by introducing a line starting with -t followed by number of threads

# restart memcached: sudo systemctl restart memcached
