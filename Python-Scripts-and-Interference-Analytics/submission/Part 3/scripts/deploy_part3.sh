

#!/bin/sh



BUCKET_NAME='lfavento'



export KOPS_STATE_STORE=gs://cca-eth-2023-group-39-$BUCKET_NAME/

PROJECT='gcloud config get-value project'

kops create -f ~/cloud-comp-arch-project/part3.yaml

kops update cluster --name part3.k8s.local --yes --admin

kops validate cluster --wait 10m

kubectl get nodes -o wide

kubectl create -f ~/Documents/GitHub/CloudComputingArch/Part3/yaml/memcache-t1-cpuset.yaml

kubectl expose pod some-memcached --name some-memcached-11211 --type LoadBalancer --port 11211 --protocol TCP
sleep 60
kubectl get service some-memcached-11211
kubectl get nodes -o wide
kubectl get pods -o wide
