#!/bin/sh

CLIENT_AGENT_NAME="sll2"
CLIENT_MEASURE_NAME="2bs1"
#INTERNAL_AGENT_IP="10.0.16.2"
#INTERNAL_MEMCACHED_IP="10.0.16.5"


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
# ./mcperf -s INTERNAL_MEMCACHED_IP -a INTERNAL_AGENT_IP --noload -T 16 -C 4 -D 4 -Q 1000 -c 4 -t 1800 --qps_interval 10 --qps_min 5000 --qps_max 100000 --qps_seed 3274
