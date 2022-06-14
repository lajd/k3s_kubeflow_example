# Note: This chart is deprecated
# https://github.com/helm/charts/tree/master/stable/hadoop

helm install hadoop  \
  --set persistence.nameNode.enabled=true  \
  --set persistence.dataNode.enabled=true  \
  --set hdfs.webhdfs.enabled=true \
  --set persistence.nameNode.storageClass=microk8s-hostpath  \
  --set persistence.dataNode.storageClass=microk8s-hostpath  \
  --set yarn.nodeManager.resources.requests.cpu=4000m \
  --set yarn.nodeManager.resources.requests.memory=4096Mi \
  stable/hadoop \
  -n admin

# Check status
kubectl exec -n admin -it hadoop-hadoop-hdfs-nn-0 -- /usr/local/hadoop/bin/hdfs dfsadmin -report

kubectl port-forward -n default hadoop-hadoop-yarn-rm-0 8088:8088

http://localhost:8088/cluster

