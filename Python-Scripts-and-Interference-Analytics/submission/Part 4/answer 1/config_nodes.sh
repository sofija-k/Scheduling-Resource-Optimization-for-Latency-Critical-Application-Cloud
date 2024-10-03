#!/bin/sh

CLIENT_AGENT_NAME="67pw"
CLIENT_MEASURE_NAME="q1cc"
#INTERNAL_AGENT_IP="10.0.16.2"
#INTERNAL_MEMCACHED_IP="10.0.16.4"


gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@client-agent-$CLIENT_AGENT_NAME --zone europe-west3-a --command="
sudo apt-get update &&
sudo apt-get install libevent-dev libzmq3-dev git make g++ --yes &&
sudo cp /etc/apt/sources.list /etc/apt/sources.list~ &&
sudo sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list &&
sudo apt-get update &&
sudo apt-get build-dep memcached --yes &&
git clone https://github.com/eth-easl/memcache-perf-dynamic.git &&
cd memcache-perf-dynamic &&
make
"

gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@client-measure-$CLIENT_MEASURE_NAME --zone europe-west3-a --command="
sudo apt-get update &&
sudo apt-get install libevent-dev libzmq3-dev git make g++ --yes &&
sudo cp /etc/apt/sources.list /etc/apt/sources.list~ &&
sudo sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list &&
sudo apt-get update &&
sudo apt-get build-dep memcached --yes &&
git clone https://github.com/eth-easl/memcache-perf-dynamic.git &&
cd memcache-perf-dynamic &&
make
"

# SSH INTO BOTH 
# client agent command : ./mcperf -T 16 -A
# client measure commands :
# ./mcperf -s INTERNAL_MEMCACHED_IP --loadonly
# ./mcperf -s INTERNAL_MEMCACHED_IP -a INTERNAL_AGENT_IP --noload -T 16 -C 4 -D 4 -Q 1000 -c 4 -t 10 --qps_interval 2 --qps_min 5000 --qps_max 100000

./mcperf -s 10.0.16.4 -a 10.0.16.2 \
--noload -T 16 -C 4 -D 4 -Q 1000 -c 4 -t 5 \
--scan 5000:125000:5000