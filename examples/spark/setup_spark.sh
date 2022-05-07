#!/bin/bash

# Ref: https://github.com/GoogleCloudPlatform/spark-on-k8s-operator#installation
helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
helm install spark-operator spark-operator/spark-operator --namespace admin

# Apply the RBAC
kubectl apply -f ./spark_rbac.yaml
