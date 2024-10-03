#!/bin/sh

BUCKET_NAME='lfavento'

gsutil mb gs://cca-eth-2023-group-39-$BUCKET_NAME/
export KOPS_STATE_STORE=gs://cca-eth-2023-group-39-$BUCKET_NAME/
export PROJECT='gcloud config get-value project'
kops create -f ~/cloud-comp-arch-project/part1.yaml
kops create secret --name part1.k8s.local sshpublickey admin -i ~/.ssh/cloud-computing.pub
kops update cluster --name part1.k8s.local --yes --admin
kops validate cluster --wait 10m
kubectl get nodes -o wide
kubectl create -f ~/cloud-comp-arch-project/memcache-t1-cpuset.yaml
kubectl expose pod some-memcached --name some-memcached-11211 --type LoadBalancer --port 11211 --protocol TCP
sleep 60
kubectl get service some-memcached-11211
kubectl get nodes -o wide
kubectl get pods -o wide
