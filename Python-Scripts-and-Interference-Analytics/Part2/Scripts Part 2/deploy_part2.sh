#!/bin/sh

BUCKET_NAME='lfavento'

export KOPS_STATE_STORE=gs://cca-eth-2023-group-39-$BUCKET_NAME/
export PROJECT='gcloud config get-value project'
kops create -f ~/cloud-comp-arch-project/part2a.yaml
kops update cluster part2a.k8s.local --yes --admin
kops validate cluster --wait 10m
kubectl get nodes -o wide
