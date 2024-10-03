#!/bin/sh

JOBS_FOLDER="/home/leonardo/Documents/GitHub/CloudComputingArch/Part3/yaml"

kubectl create -f $JOBS_FOLDER/parsec-ferret.yaml
kubectl create -f $JOBS_FOLDER/parsec-canneal.yaml
kubectl create -f $JOBS_FOLDER/parsec-dedup.yaml
kubectl create -f $JOBS_FOLDER/parsec-blackscholes.yaml
kubectl create -f $JOBS_FOLDER/parsec-freqmine.yaml
kubectl create -f $JOBS_FOLDER/parsec-radix.yaml
kubectl create -f $JOBS_FOLDER/parsec-vips.yaml

# kubectl get pods -o json > results.json
# python3 get_time.py results.json
