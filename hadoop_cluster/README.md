docker: 
https://hub.docker.com/r/apache/hadoop
# install pkg:

# Create create permission for hive volumns
mkdir -p ./hadoop_cluster/volumes/warehouse
sudo chown 1000:1000 ./hadoop_cluster/volumes/warehouse
chmod 777 ./hadoop_cluster/volumes/warehouse

docker compose up 

- Namenode: http://localhost:9870/
- ResourceManager: http://localhost:8089/
- Superset: http://127.0.0.1:8088/
```

# TODO:
- mount volumns out
- permission to write file