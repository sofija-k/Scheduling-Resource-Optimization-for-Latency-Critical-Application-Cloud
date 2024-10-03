#!/bin/sh

CLIENT_AGENT_NAME="f3ww"
CLIENT_MEASURE_NAME="ztf5"
#INTERNAL_AGENT_IP="10.0.16.5"
#MEMCACHED_IP="100.96.3.2"

gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@client-agent-$CLIENT_AGENT_NAME \
--zone europe-west3-a --command="
sudo apt-get update &&
sudo apt-get install libevent-dev libzmq3-dev git make g++ --yes &&
sudo cp /etc/apt/sources.list /etc/apt/sources.list~ &&
sudo sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list &&
sudo apt-get update &&
sudo apt-get build-dep memcached --yes &&
cd && git clone https://github.com/shaygalon/memcache-perf.git &&
cd memcache-perf || exit &&
git checkout 0afbe9b &&
make
"

gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@client-measure-"$CLIENT_MEASURE_NAME" \
--zone europe-west3-a --command="
sudo apt-get update &&
sudo apt-get install libevent-dev libzmq3-dev git make g++ --yes &&
sudo cp /etc/apt/sources.list /etc/apt/sources.list~ &&
sudo sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list &&
sudo apt-get update &&
sudo apt-get build-dep memcached --yes &&
cd && git clone https://github.com/shaygalon/memcache-perf.git &&
cd memcache-perf || exit &&
git checkout 0afbe9b &&
make
"

# SSH INTO BOTH 
# client agent command : ./mcperf -T 16 -A
# client measure commands :
# ./mcperf -s MEMCACHED_IP --loadonly
# ``./mcperf -s MEMCACHED_IP -a INTERNAL_AGENT_IP \
# --noload -T 16 -C 4 -D 4 -Q 1000 -c 4 -w 2 -t 5 \
# --scan 30000:110000:5000

