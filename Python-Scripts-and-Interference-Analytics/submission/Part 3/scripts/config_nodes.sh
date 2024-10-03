#!/bin/sh

CLIENT_AGENT_A_NAME="r658"
CLIENT_AGENT_B_NAME="8xj4"
CLIENT_MEASURE_NAME="3sw7"
#INTERNAL_AGENT_A_IP="10.0.16.3"
#INTERNAL_AGENT_B_IP="10.0.16.2"
#MEMCACHED_IP="100.96.3.2"

gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@client-agent-a-$CLIENT_AGENT_A_NAME --zone europe-west3-a --command="
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

gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@client-agent-b-$CLIENT_AGENT_B_NAME --zone europe-west3-a --command="
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

gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@client-measure-"$CLIENT_MEASURE_NAME" --zone europe-west3-a --command="
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
# client agent a command : ./mcperf -T 2 -A
# client agent b command : ./mcperf -T 4 -A
# client measure commands :
# ./mcperf -s MEMCACHED_IP --loadonly
# ./mcperf -s MEMCACHED_IP -a INTERNAL_AGENT_A_IP -a INTERNAL_AGENT_B_IP --noload -T 6 -C 4 -D 4 -Q 1000 -c 4 -t 10 --scan 30000:30500:5

