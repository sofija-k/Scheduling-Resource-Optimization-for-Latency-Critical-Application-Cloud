#!/bin/sh



BUCKET_NAME='pabdel'



export KOPS_STATE_STORE=gs://cca-eth-2023-group-39-$BUCKET_NAME/

PROJECT='gcloud config get-value project'

kops create -f ~/Desktop/Cloud\ Computing/cloud-comp-arch-project/part4.yaml

kops update cluster --name part4.k8s.local --yes --admin

kops validate cluster --wait 10m

kubectl get nodes -o wide
