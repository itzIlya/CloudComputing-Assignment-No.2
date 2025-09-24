# Cloud Computing HW2

# Abstract

This is a PDF of a notion document for Homework 2 of the Cloud_Computing-Spring-2025 course at Shiraz University located [here](https://github.com/mmRoshani/cloud-computing-2025/tree/main/homeworks/two). The full notion document is available at the below link:

[https://www.notion.so/Cloud-Computing-HW2-1c8fff288ff18035bc00c236285a6e3f?pvs=4](https://www.notion.so/Cloud-Computing-HW2-1c8fff288ff18035bc00c236285a6e3f?pvs=21)

# Part 1

## Definition and explanation of core concepts

Here are some explanations regarding different concepts in map reduce:

### Map

The **Map** phase takes an input dataset and applies a function to each individual element, transforming it into intermediate key-value pairs. The input data for the map function can be in the form of files (e.g., text, binary, etc.). These files are split into chunks (blocks), and each chunk is processed by different map tasks running in parallel. The result of the Map function is a set of key-value pairs, typically unordered. Each key can appear multiple times with different associated values.

### Shuffle

The **Shuffle** phase sorts and groups the key-value pairs output by the Map phase. It essentially involves redistributing the data based on keys to ensure that all the values associated with the same key are grouped together. his phase involves significant data transfer between different machines in the cluster (from map tasks to reduce tasks). This is often the most resource-intensive phase of a MapReduce job. Shuffling can be accomplished by hashing part of the data and distributing the resulted hash across a series of nodes that are going to perform the reduce phase.

### Reduce

The **Reduce** phase takes the grouped key-value pairs from the shuffle phase and applies a function to aggregate them. Each reducer processes all the values for a particular key.

## Hadoop: Core Modules

### HDFS

HDFS is the storage layer of Hadoop, designed to store vast amounts of data across a distributed environment. It splits large files into fixed-size blocks and stores these blocks across multiple machines in a cluster.

**Core Concepts**:

- **Blocks**: Data is divided into large blocks (typically 128 MB or 256 MB), and these blocks are distributed across the cluster.
- **Replication**: Data blocks are replicated across multiple nodes to ensure fault tolerance. By default, each block is replicated 3 times.
- **NameNode and DataNode**:
    - **NameNode**: It is the master that manages the file system’s metadata, such as which files are stored on which DataNodes.
    - **DataNode**: These are the worker nodes that store the actual data blocks.

### YARN

YARN is the resource management layer of Hadoop. It handles job scheduling and cluster resource management.

**Core Concepts**:

- **ResourceManager**: It is the master daemon that manages resource allocation across all jobs in the cluster. It maintains a global view of available resources.
- **NodeManager**: Each worker node has a NodeManager that reports the node’s resource usage and health to the ResourceManager.
- **ApplicationMaster**: Each application (e.g., MapReduce job) has its own ApplicationMaster, which negotiates resources with the ResourceManager and manages task execution.

### MapReduce

MapReduce is the computation framework within Hadoop that performs distributed data processing tasks. It breaks down tasks into the Map and Reduce phases as described earlier.

**Core Concepts**:

- **JobTracker**: The JobTracker is the master process that manages the execution of MapReduce jobs. It schedules the tasks (maps and reduces) on available nodes.
- **TaskTracker**: The TaskTracker runs on the worker nodes and executes the map and reduce tasks assigned by the JobTracker.

## Spark: Core Concepts

### RDDs

RDDs are the core abstraction in Spark for distributed data processing. They represent an immutable, distributed collection of objects that can be processed in parallel across a cluster. RDDs are fault-tolerant; if any partition of an RDD is lost, it can be recomputed using lineage information (the sequence of operations that created it). 

RDDs support two types of operations:

- **Transformations**: Operations that produce new RDDs from existing ones (e.g., `map`, `filter`, `groupBy`).
- **Actions**: Operations that return a result to the driver or write data to external storage (e.g., `collect`, `count`, `save`).

The data is not actually processed unless an action is executed. Transformations will just create new RDDs and the data won’t change or no new data is generated. 

### Data frames

They are a higher-level abstraction in Spark built on top of RDDs. They are distributed collections of data organized into named columns, similar to tables in a relational database. Spark SQL allows users to query structured data using SQL queries. It integrates with DataFrames, enabling users to perform complex analytics using both SQL and Spark's built-in operations.

### Spark Modes

Spark can run in multiple modes, including **Standalone Mode** (running on a single machine), **Cluster Mode** (running on a cluster managed by YARN or Mesos), and **Local Mode** (running on a single machine using multiple threads).

### Computation in Spark

Spark performs computations in memory, which reduces the need to write intermediate results to disk. This results in faster execution, especially for iterative algorithms (such as in machine learning or federated learning) that require multiple stages of computation.

## Hadoop & MapReduce relationship

### **Hadoop as Infrastructure**:

Hadoop provides the infrastructure for distributed storage and resource management, while **MapReduce** is a programming model and computational framework for processing data in parallel across a cluster.

### **HDFS (Hadoop Distributed File System)**:

MapReduce relies on HDFS for data storage. It processes data that is distributed across the Hadoop cluster, with the data being split into blocks stored on various worker nodes. MapReduce jobs are designed to process this data in parallel.

### **YARN (Yet Another Resource Negotiator)**

YARN manages the resources needed for MapReduce jobs. When a MapReduce job is submitted, the ResourceManager allocates resources across the cluster, and the ApplicationMaster ensures that the map and reduce tasks are scheduled and executed on available nodes.

### **MapReduce in Hadoop**

**MapReduce** leverages Hadoop's resource management (via YARN) and distributed storage (via HDFS) to process large datasets. It breaks down tasks into smaller jobs (map and reduce), distributes them across worker nodes, and combines the results after all tasks have been completed.

## Using docker to run Hadoop and Spark

I have done this in the tasks part in tasks 1 and 2.

# Part 2: Comparative Analysis

### Speed

The key reason behind Spark's superior speed is its in-memory computation model. Spark performs intermediate computations in memory, which reduces the need to read and write data to disk between stages of a job. This significantly speeds up iterative algorithms (e.g., machine learning, graph processing), which require multiple rounds of computation on the same dataset. By avoiding disk I/O between stages of computation and utilizing memory as storage, Spark can execute jobs much faster than Hadoop MapReduce. In Hadoop, MapReduce tasks are disk-intensive. Each intermediate result from the map phase is written to disk before it’s passed to the reduce phase. This I/O bottleneck makes Hadoop slower, especially for jobs that require multiple stages of computation or iterative algorithms.
So in terms of speed, I would not expect much difference between the two if our task was just a one time computation of a batch operation since keeping things in memory and RDDs and the other things that Spark does don’t really give it a significant edge in relation to Hadoop. However, if the task was something that needed to handle iterative processing, such as task 2 of this homework,👀, Spark would definitely be much more suited for that job. (I had already completed Part 3 of this homework and all of its tasks before answering Part 1 & 2 so I already had something in mind about the different types of tasks that can be given to the two.)

### Data handling

Spark uses **RDDs and DataFrames** which are more flexible and support advanced features like caching, transformations, and optimizations. **HDFS** in Hadoop, on the other hand, is just a file system designed for storing large datasets, while **MapReduce** in Hadoop is used to process data as key-value pairs. In Hadoop, data is stored and processed on disk, while in Spark, much of the data is stored in memory, making it much faster for certain types of processing.

### Typical Use Cases Where Each Technology Excels

**Batch processing:** Hadoop is best suited for **batch processing** large datasets where speed is not the primary concern. Its disk-based processing makes it well-suited for large-scale ETL jobs (extract, transform, load), data aggregation, and log analysis. 
While Spark can be used for batch processing, it truly shines in **iterative processing** (e.g., machine learning and graph processing). Its in-memory processing model allows for multiple iterations on the same data without the need for costly disk writes in between. Tasks such as Task 2 of this homework (Federated Learning) may be more efficiently handled on Spark than on Hadoop.

**Large-scale Data Processing**: Hadoop is often used for data warehousing, large-scale data storage, and jobs that involve simple, linear processing over huge datasets. For example, it is commonly used for processing large amounts of unstructured data, such as logs and clickstream data.

**Real-time Processing**: Spark’s ability to perform **real-time stream processing** (using Spark Streaming) is a major advantage over Hadoop. This makes it suitable for applications that require low-latency data processing, such as real-time analytics, fraud detection, and monitoring.

**Interactive Analytics**: With its ability to run in-memory, Spark supports interactive queries and ad-hoc data analysis. It is ideal for environments where users need fast feedback from their computations, like in data science and machine learning.

# Part 3

## Task 1

For running the hdfs cluster on docker we first clone this repository:
https://github.com/bigdatafoundation/docker-hadoop/tree/master

[https://github.com/bigdatafoundation/docker-hadoop.git](https://github.com/bigdatafoundation/docker-hadoop.git)

We use the 3.3.6 version for this HW.

Ignoring what is said in the repository’s .README file, we change the docker-compose.yml of the project:

```bash
version: "3.7"
services:
  namenode:
    image: cjj2010/hadoop:3.3.6
    ports: 
        - "9870:9870"
        #- "8088:8088"
    command: > 
      bash -c "hdfs namenode & yarn resourcemanager "
    hostname: hdfs-namenode

  datanode:
    image: cjj2010/hadoop:3.3.6
    hostname: datanode
    depends_on: 
        - namenode
    command: >
      bash -c "hdfs datanode & yarn nodemanager "
    ports:
# The host port is randomly assigned by Docker, to allow scaling to multiple DataNodes on the same host
      - "9864"
    links:
        - namenode:hdfs-namenode

  secondarynamenode:
    image: cjj2010/hadoop:3.3.6
    command: hdfs secondarynamenode
    ports:
        - "9868:9868"
    links:
        - namenode:hdfs-namenode

  yarn:
    image: gelog/hadoop
    container_name: yarn
    hostname: yarn
    command: start-yarn.sh
    ports:
      - "8088:8088"
      - "8042:8042"
    depends_on:
      - namenode
      - datanode

```

We changed it so that it adds yarn to the set of docker containers that make up our cluster and also remove the useless port dedicated to the namenode and give it to yarn.

next all we have to do is enter the `docker-compose up -d` command to run the hadoop cluster as a service.

Once the cluster is up, we should copy our files to the namenode container. There are 3 files we need to have a MapReduce job. The mapper, the reducer and the data. Writing the mapper and reducer in python, we also have our dataset ready in the data.csv file.

```bash
#!/usr/bin/env python3
import sys

def main():
    for line in sys.stdin:

        try:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) == 3:
                client_id, feature_value, _ = parts
                # Possibly check if they are valid or skip if not
                if client_id == "client_id" and feature_value == "feature_value":
                    continue

                print("{}\t{},1".format(client_id, feature_value))
        except Exception as e:
            sys.stderr.write("Exception in mapper: {}\n".format(str(e)))
            sys.stderr.write("Offending line: {}\n".format(line))
            exit(2)

if __name__ == "__main__":
    main()

```

```bash
#!/usr/bin/env python3
import sys

def main():
    current_client = None
    sum_feature_values = 0.0
    count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        # Example line => "client1    10.5,1"
        client_id, value_str = line.split('\t', 1)
        
        # value_str => "10.5,1"
        feature_value_str, occur_str = value_str.split(',', 1)
        
        try:
            feature_value = float(feature_value_str)
            occur = int(occur_str)
        except ValueError:
            # If there's parsing error, skip or handle gracefully
            continue

        if current_client == client_id:
            # Same client_id; accumulate
            sum_feature_values += feature_value
            count += occur
        else:
            # New client_id; output the previous client's aggregates first
            if current_client is not None:
                print("{}\t{}\t{}".format(current_client, sum_feature_values, count))

            # Reset for the new client_id
            current_client = client_id
            sum_feature_values = feature_value
            count = occur

    # Print the last client’s result if it exists
    if current_client is not None:
        print("{}\t{}\t{}".format(current_client, sum_feature_values, count))

if __name__ == "__main__":
    main()

```

We first need to get these files into the namenode container and then put the in HDFS so that we can tell hadoop to run the mapreduce job. What pretty much happens is that we only need to write the mapper and reducer scripts and give them to hadoop and it will then take it from there and handle everything from there. We don’t need to worry about how the job gets distributed or where each part of the computation happens. 

So, first we need to put all three files inside the namenode container using:

```bash
docker cp <file_path> <container_id>:<Path_inside_the_container>
```

![image.png](image.png)

We also do the same for data.csv.

After all the files are inside the container, we should put the data that we want to perform our computation on inside the HDFS. Working with the HDFS happens in the docker container with commands that start with `hdfs` .

Now we first need to create a directory in HDFS to put our files in. Generally, some of the Linux terminal tools are available using a tag after writing `hdfs dfs` .

```bash
hdfs dfs -mkdir /user/ilya/
```

Then, we put the data.csv file into the newly created directory from the directory in container using the below command.

```bash
hdfs dfs -put /tmp/data.csv /user/ilya/
```

So here is the location of all of files:

- [mapper.py](http://mapper.py) : namenode_container:/mapper.py
- [reducer.py](http://reducer.py) : namenode_container:/reducer.py
- data.csv : hdfs:/user/ilya/data.csv

![image.png](./images/image%201.png)

![image.png](./images/image%202.png)

Finally, we enter the below command to run the MapReduce job:

```bash
  hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -files mapper.py,reducer.py \
    -mapper  mapper.py \
    -reducer reducer.py \
    -input /user/ilya/data.csv \
    -output /user/ilya/output3
```

![image.png](./images/image%203.png)

![image.png](./images/image%204.png)

![image.png](./images/image%205.png)

Now that the MapReduce job is done, we can see the output in the directory we previously specified to hdfs which in this case is /user/ilya/output3.

![image.png](./images/image%206.png)

and that is it for task1.

## Task 2

Now for task 2 I switched to the big-data-europe repository:
https://github.com/big-data-europe/docker-hadoop

[https://github.com/big-data-europe/docker-hadoop.git](https://github.com/big-data-europe/docker-hadoop.git)

Now to my understanding, the big-data-europe repo is a bit old and uses a probably outdated image of debian 9. This leads to the apt package manager not working properly since the Linux image is outdated an is now in a EOL (End of Life) state and the package manager has to look in the old archived links to look for packages. In order to allow it to look for old packages I had to change the docker files and a

```bash
# hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
   -files mapper.py,reducer.py \
    -mapper  mapper.py \
    -reducer reducer.py \
    -input /user/ilya/data.csv \
    -output /user/ilya/output3
> > > > > ^C# ^C
# ^C
# 
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
   -files mapper.py,reducer.py \
    -mapper  mapper.py \
    -reducer reducer.py \
    -input /user/ilya/data.csv \
    -output /user/ilya/output2# > > > > > 
packageJobJar: [/tmp/hadoop-unjar1288458226019370508/] [] /tmp/streamjob8159985081782657550.jar tmpDir=null
2025-04-02 08:28:19,955 INFO client.RMProxy: Connecting to ResourceManager at resourcemanager/172.19.0.2:8032
2025-04-02 08:28:20,295 INFO client.AHSProxy: Connecting to Application History server at historyserver/172.19.0.5:10200
2025-04-02 08:28:20,334 INFO client.RMProxy: Connecting to ResourceManager at resourcemanager/172.19.0.2:8032
2025-04-02 08:28:20,334 INFO client.AHSProxy: Connecting to Application History server at historyserver/172.19.0.5:10200
2025-04-02 08:28:20,659 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/root/.staging/job_1743581296563_0002
2025-04-02 08:28:20,925 INFO sasl.SaslDataTransferClient: SASL encryption trust check: localHostTrusted = false, remoteHostTrusted = false
2025-04-02 08:28:21,124 INFO sasl.SaslDataTransferClient: SASL encryption trust check: localHostTrusted = false, remoteHostTrusted = false
2025-04-02 08:28:21,590 INFO sasl.SaslDataTransferClient: SASL encryption trust check: localHostTrusted = false, remoteHostTrusted = false
2025-04-02 08:28:21,713 INFO mapred.FileInputFormat: Total input files to process : 1
2025-04-02 08:28:21,784 INFO sasl.SaslDataTransferClient: SASL encryption trust check: localHostTrusted = false, remoteHostTrusted = false
2025-04-02 08:28:22,232 INFO sasl.SaslDataTransferClient: SASL encryption trust check: localHostTrusted = false, remoteHostTrusted = false
2025-04-02 08:28:22,665 INFO mapreduce.JobSubmitter: number of splits:2
2025-04-02 08:28:22,955 INFO sasl.SaslDataTransferClient: SASL encryption trust check: localHostTrusted = false, remoteHostTrusted = false
2025-04-02 08:28:22,995 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1743581296563_0002
2025-04-02 08:28:22,995 INFO mapreduce.JobSubmitter: Executing with tokens: []
2025-04-02 08:28:23,319 INFO conf.Configuration: resource-types.xml not found
2025-04-02 08:28:23,319 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
2025-04-02 08:28:23,666 INFO impl.YarnClientImpl: Submitted application application_1743581296563_0002
2025-04-02 08:28:23,726 INFO mapreduce.Job: The url to track the job: http://resourcemanager:8088/proxy/application_1743581296563_0002/
2025-04-02 08:28:23,734 INFO mapreduce.Job: Running job: job_1743581296563_0002
2025-04-02 08:28:32,914 INFO mapreduce.Job: Job job_1743581296563_0002 running in uber mode : false
2025-04-02 08:28:32,919 INFO mapreduce.Job:  map 0% reduce 0%
2025-04-02 08:28:41,117 INFO mapreduce.Job:  map 100% reduce 0%
2025-04-02 08:28:48,214 INFO mapreduce.Job:  map 100% reduce 100%
2025-04-02 08:28:49,257 INFO mapreduce.Job: Job job_1743581296563_0002 completed successfully
2025-04-02 08:28:49,415 INFO mapreduce.Job: Counters: 54
        File System Counters
                FILE: Number of bytes read=517
                FILE: Number of bytes written=699461
                FILE: Number of read operations=0
                FILE: Number of large read operations=0
                FILE: Number of write operations=0
                HDFS: Number of bytes read=4745
                HDFS: Number of bytes written=78
                HDFS: Number of read operations=11
                HDFS: Number of large read operations=0
                HDFS: Number of write operations=2
                HDFS: Number of bytes read erasure-coded=0
        Job Counters 
                Launched map tasks=2
                Launched reduce tasks=1
                Rack-local map tasks=2
                Total time spent by all maps in occupied slots (ms)=32272
                Total time spent by all reduces in occupied slots (ms)=36408
                Total time spent by all map tasks (ms)=8068
                Total time spent by all reduce tasks (ms)=4551
                Total vcore-milliseconds taken by all map tasks=8068
                Total vcore-milliseconds taken by all reduce tasks=4551
                Total megabyte-milliseconds taken by all map tasks=33046528
                Total megabyte-milliseconds taken by all reduce tasks=37281792
        Map-Reduce Framework
                Map input records=173
                Map output records=172
                Map output bytes=2580
                Map output materialized bytes=581
                Input split bytes=182
                Combine input records=0
                Combine output records=0
                Reduce input groups=3
                Reduce shuffle bytes=581
                Reduce input records=172
                Reduce output records=3
                Spilled Records=344
                Shuffled Maps =2
                Failed Shuffles=0
                Merged Map outputs=2
                GC time elapsed (ms)=293
                CPU time spent (ms)=3450
                Physical memory (bytes) snapshot=858296320
                Virtual memory (bytes) snapshot=18668240896
                Total committed heap usage (bytes)=761790464
                Peak Map Physical memory (bytes)=317558784
                Peak Map Virtual memory (bytes)=5110484992
                Peak Reduce Physical memory (bytes)=225505280
                Peak Reduce Virtual memory (bytes)=8450256896
        Shuffle Errors
                BAD_ID=0
                CONNECTION=0
                IO_ERROR=0
                WRONG_LENGTH=0
                WRONG_MAP=0
                WRONG_REDUCE=0
        File Input Format Counters 
                Bytes Read=4563
        File Output Format Counters 
                Bytes Written=78
2025-04-02 08:28:49,415 INFO streaming.StreamJob: Output directory: /user/ilya/output2
```

![image.png](./images/image%207.png)

We can see the results are the same as the ones in the previous task. This was just to make sure that BDE works. 

### Things went wrong:

Now I later learned that the default compose file in the BDE repo wasn’t configured for Spark and there was another docker-compose file in the [readme.md](http://readme.md) of the repo that sets up a spark cluster. So the above step might have been useless…

### Moving Forward :)

For the remainder of task 2 I didn’t use the docker-compose.yml file that was in the repository’s directory. Instead, I used the file that was in the repo’s [README.md](http://README.md) file:

```docker
version: '3'
services:
  spark-master:
    image: bde2020/spark-master:3.3.0-hadoop3.3
    container_name: spark-master
    ports:
      - "8080:8080"
      - "7077:7077"
    environment:
      - INIT_DAEMON_STEP=setup_spark
  spark-worker-1:
    image: bde2020/spark-worker:3.3.0-hadoop3.3
    container_name: spark-worker-1
    depends_on:
      - spark-master
    ports:
      - "8081:8081"
    environment:
      - "SPARK_MASTER=spark://spark-master:7077"
  spark-worker-2:
    image: bde2020/spark-worker:3.3.0-hadoop3.3
    container_name: spark-worker-2
    depends_on:
      - spark-master
    ports:
      - "8082:8081"
    environment:
      - "SPARK_MASTER=spark://spark-master:7077"
  spark-history-server:
      image: bde2020/spark-history-server:3.3.0-hadoop3.3
      container_name: spark-history-server
      depends_on:
        - spark-master
      ports:
        - "18081:18081"
      volumes:
        - /tmp/spark-events-local:/tmp/spark-events
```

This docker-compose.yml file allows us to use spark since the previous file didn’t have any spark master or workers. This one sets up a spark-master, a spark history server and two spark workers. However, when I tried to work with this compose file, I encountered some issues later on that kept the workers from registering with the master. This was because the master container was started **without an explicit hostname**, so inside the container Spark picks the Docker‑generated hostname (the short container ID). This means that the master believes that its url is something like `spark://b04385a40d04:7077` but the workers keep trying to contact the master using `spark-master:7077`, so they resolve “spark-master” and connect, but the master immediately answers “my real URL is `spark://b04385a40d04:7077` – reconnect!” So I modified the docker-compose file so that it explicitly species the hostname for the master.

```docker
version: '3'
services:
  spark-master:
    image: bde2020/spark-master:3.3.0-hadoop3.3
    container_name: spark-master
    hostname: spark-master                # (optional, but guarantees /etc/hostname)
    environment:
      - SPARK_MASTER_HOST=spark-master    # <- forces advertised host
      - INIT_DAEMON_STEP=setup_spark
    ports:
      - "8080:8080"
      - "7077:7077"

  spark-worker-1:
    image: bde2020/spark-worker:3.3.0-hadoop3.3
    container_name: spark-worker-1
    depends_on:
      - spark-master
    ports:
      - "8081:8081"
    environment:
      - "SPARK_MASTER=spark://spark-master:7077"
  spark-worker-2:
    image: bde2020/spark-worker:3.3.0-hadoop3.3
    container_name: spark-worker-2
    depends_on:
      - spark-master
    ports:
      - "8082:8081"
    environment:
      - "SPARK_MASTER=spark://spark-master:7077"
  spark-history-server:
      image: bde2020/spark-history-server:3.3.0-hadoop3.3
      container_name: spark-history-server
      depends_on:
        - spark-master
      ports:
        - "18081:18081"
      volumes:
        - /tmp/spark-events-local:/tmp/spark-events
```

Now the the docker container is setup, all we have to is just say docker-compose up -d and we have ourselves a spark cluster with 4 nodes 🙂

![image.png](./images/image%208.png)

## The Script

Now for running the spark job, we first need a script:

```python
#!/usr/bin/env python3
from pyspark.sql import SparkSession
import random

# Initialize SparkSession 
spark = SparkSession.builder \
    .appName("FederatedAveraging") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

sc = spark.sparkContext

# If we were to use the same containers for both tasks we could use the below 
# code to extract tghe results from the previous task.
'''
lines = sc.textFile("hdfs://hdfs-namenode:9000/user/ilya/output2/part-00000")
aggregated_data = lines.map(lambda line: line.strip().split()) \
                     .map(lambda parts: (parts[0], (float(parts[1]), int(parts[2]))))
''' 

# Here I just copied the results from task 1 and hardcoded them into the code since 
# I am running the two tasks on two different containers
aggregated_data = sc.parallelize([
    ("client1", (2197.6, 58)),
    ("client2", (2381.9, 57)),
    ("client3", (2568.6, 57))
])
# The above is an example of an RDD!

# Calculate the initial global average
total_sum = aggregated_data.map(lambda x: x[1][0]).sum()
total_count = aggregated_data.map(lambda x: x[1][1]).sum()
global_avg = total_sum / total_count
print("Initial Global Average: {:.4f}".format(global_avg))

# Simulate federated averaging for 3 rounds as it is said the in the task2 readme
num_rounds = 3 
for round_num in range(1, num_rounds + 1):
    # Compute local averages for each client
    local_averages = aggregated_data.map(lambda x: (x[0], x[1][0] / x[1][1])).collect()
    print("Round {} Local Averages:".format(round_num), local_averages)
    
    # Simulate local update by adding a small random value
    updated_averages = [(client, avg + random.uniform(-1, 1)) for client, avg in local_averages]
    print("Round {} Updated Local Averages:".format(round_num), updated_averages)
    
    # Recalculate global average from these updated local averages
    new_global_avg = sum(avg for client, avg in updated_averages) / len(updated_averages)
    print("Round {} Global Average: {:.4f}".format(round_num, new_global_avg))
    
spark.stop()

```

Now since I changed the containers that I was working with when I was completing the mapreduce job, I can’t get the results from the mapreduce job directly through the containers. So what I did was that I just took the results form the mapreduce job above and just hard coded them into the federated averaging python script. (I also rounded the results to one decimal point)

Similar to the script provided in the homework description for task2, we first compute the initial global average. map extracts the sum part in the result from mapreduce and then sum() reduces them to a single number. 

In the above code, the variable aggregated_data is an RDD. Which has three tuples inside it. When we call the map function, we create a new RDD which only contains 2197.6, 2381.9 and 2568.6. The map function is a transformation. When we call sum(), we are performing an action an are pretty much performing a distributed reduction.

Now in the loop we iterate for three rounds performing a simulation of federated averaging. local_averages shows each client’s current local average and then collects the result and gives it back to the driver for printing. We then fake a local training update by adding a random value to the local average of each client. Finally we update the global average using the new local averages. Keep in mind that this script does not feed the updates back into the RDD and is only a read only simulation. Perhaps in real world cases we may would write the new global model back to each client to perform some new update for each client.

And that’s it for the script. We then named the script [`FederatedAveraging.py`](http://FederatedAveraging.py).  All is left is to run in it.

## Running the Script

big-data-europe has a Spark Python template in its repository located at [this link](https://github.com/big-data-europe/docker-spark/tree/master/template/python). It tells us to packatge our application using pip, and create a separate docker image outsite the current spark cluster that we already have, build and run it using a command that they have in their readme file. And so, I created a new directory, put the [FederatedAveraging.py](http://FederatedAveraging.py) script in it, along with a Dockerfile and a requirements.txt file and then named it `./my-spark-app/` . Here are the contents of the Dockerfile:

```python
		FROM bde2020/spark-python-template:3.3.0-hadoop3.3

    MAINTAINER Ilya iatashdowda@gmail.com
   
    COPY . /app
    
		RUN pip install -r /app/requirements.txt
    
    ENV SPARK_APPLICATION_PYTHON_LOCATION=/app/FederatedAveraging.py
    
```

It looks pretty much like the template provided by the bde repo.

Now we just have to make sure our spark cluster is up and running and all the containers are on the same network: 

![image.png](./images/image%209.png)

![image.png](./images/image%2010.png)

in the spark UI we can also see that we now have two workers available. All is left is to just run the spark job.

We run the job using the following command:

```python
docker run --rm --name my-spark-app --network docker-hadoop_default    -e SPARK_MASTER_URL=spark-master   -e SPARK_APPLICATION_PYTHON_LOCATION=/app/FederatedAveraging.py my-spark-app
```

Some important notes for the command:

- YOU HAVE TO SPECIFY THE PROPER NETWORK!!!! Well at least I had to… Because when i didn’t the container cloud not contact the spark-master container. The container name is docker-hadoop_default or spark_defualt or something similar. to view all the networks you can enter the command I have entered in an image above:
    
    The first one is to just view all the available networks and the second one to see which network each container is on.
    
    ```powershell
    docker network ls
    docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Networks}}'
    ```
    
- 

Here is the output:

```python
 C:\Users\Ilya\Desktop\programming\sem6\CHW2\docker-hadoop\my-spark-app> docker run --rm --name my-spark-app --network docker-hadoop_default    -e SPARK_MASTER_URL=spark-master   -e SPARK_APPLICATION_PYTHON_LOCATION=/app/FederatedAveraging.py my-spark-app
Submit application /app/FederatedAveraging.py to Spark master spark://spark-master:7077
Passing arguments
25/04/17 13:00:25 INFO SparkContext: Running Spark version 3.3.0
25/04/17 13:00:25 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
25/04/17 13:00:25 INFO ResourceUtils: ==============================================================
25/04/17 13:00:25 INFO ResourceUtils: No custom resources configured for spark.driver.
25/04/17 13:00:25 INFO ResourceUtils: ==============================================================
25/04/17 13:00:25 INFO SparkContext: Submitted application: FederatedAveraging
25/04/17 13:00:25 INFO ResourceProfile: Default ResourceProfile created, executor resources: Map(cores -> name: cores, amount: 1, script: , vendor: , memory -> name: memory, amount: 1024, script: , vendor: , offHeap -> name: offHeap, amount: 0, script: , vendor: ), task resources: Map(cpus -> name: cpus, amount: 1.0)
25/04/17 13:00:25 INFO ResourceProfile: Limiting resource is cpu
25/04/17 13:00:25 INFO ResourceProfileManager: Added ResourceProfile id: 0
25/04/17 13:00:25 INFO SecurityManager: Changing view acls to: root
25/04/17 13:00:25 INFO SecurityManager: Changing modify acls to: root
25/04/17 13:00:25 INFO SecurityManager: Changing view acls groups to:
25/04/17 13:00:25 INFO SecurityManager: Changing modify acls groups to:
25/04/17 13:00:25 INFO SecurityManager: SecurityManager: authentication disabled; ui acls disabled; users  with view permissions: Set(root); groups with view permissions: Set(); users  with 
modify permissions: Set(root); groups with modify permissions: Set()
25/04/17 13:00:25 INFO Utils: Successfully started service 'sparkDriver' on port 45091.
25/04/17 13:00:25 INFO SparkEnv: Registering MapOutputTracker
25/04/17 13:00:26 INFO SparkEnv: Registering BlockManagerMaster
25/04/17 13:00:26 INFO BlockManagerMasterEndpoint: Using org.apache.spark.storage.DefaultTopologyMapper for getting topology information
25/04/17 13:00:26 INFO BlockManagerMasterEndpoint: BlockManagerMasterEndpoint up
25/04/17 13:00:26 INFO SparkEnv: Registering BlockManagerMasterHeartbeat
25/04/17 13:00:26 INFO DiskBlockManager: Created local directory at /tmp/blockmgr-1e8726ca-1b66-4495-889b-9615261cfdbb
25/04/17 13:00:26 INFO MemoryStore: MemoryStore started with capacity 366.3 MiB
25/04/17 13:00:26 INFO SparkEnv: Registering OutputCommitCoordinator
25/04/17 13:00:26 INFO Utils: Successfully started service 'SparkUI' on port 4040.
25/04/17 13:00:26 INFO StandaloneAppClient$ClientEndpoint: Connecting to master spark://spark-master:7077...
25/04/17 13:00:26 INFO TransportClientFactory: Successfully created connection to spark-master/172.19.0.2:7077 after 33 ms (0 ms spent in bootstraps)
25/04/17 13:00:26 INFO StandaloneSchedulerBackend: Connected to Spark cluster with app ID app-20250417130026-0001
25/04/17 13:00:26 INFO StandaloneAppClient$ClientEndpoint: Executor added: app-20250417130026-0001/0 on worker-20250417125059-172.19.0.3-42417 (172.19.0.3:42417) with 8 core(s)
25/04/17 13:00:26 INFO StandaloneSchedulerBackend: Granted executor ID app-20250417130026-0001/0 on hostPort 172.19.0.3:42417 with 8 core(s), 1024.0 MiB RAM
25/04/17 13:00:26 INFO StandaloneAppClient$ClientEndpoint: Executor added: app-20250417130026-0001/1 on worker-20250417125059-172.19.0.4-45955 (172.19.0.4:45955) with 8 core(s)
25/04/17 13:00:26 INFO Utils: Successfully started service 'org.apache.spark.network.netty.NettyBlockTransferService' on port 41229.
25/04/17 13:00:26 INFO NettyBlockTransferService: Server created on abc55cc386c2:41229
25/04/17 13:00:26 INFO StandaloneSchedulerBackend: Granted executor ID app-20250417130026-0001/1 on hostPort 172.19.0.4:45955 with 8 core(s), 1024.0 MiB RAM
25/04/17 13:00:26 INFO BlockManager: Using org.apache.spark.storage.RandomBlockReplicationPolicy for block replication policy
25/04/17 13:00:26 INFO BlockManagerMaster: Registering BlockManager BlockManagerId(driver, abc55cc386c2, 41229, None)
25/04/17 13:00:26 INFO BlockManagerMasterEndpoint: Registering block manager abc55cc386c2:41229 with 366.3 MiB RAM, BlockManagerId(driver, abc55cc386c2, 41229, None)
25/04/17 13:00:26 INFO BlockManagerMaster: Registered BlockManager BlockManagerId(driver, abc55cc386c2, 41229, None)
25/04/17 13:00:26 INFO BlockManager: Initialized BlockManager: BlockManagerId(driver, abc55cc386c2, 41229, None)
25/04/17 13:00:26 INFO StandaloneAppClient$ClientEndpoint: Executor updated: app-20250417130026-0001/1 is now RUNNING
25/04/17 13:00:26 INFO StandaloneAppClient$ClientEndpoint: Executor updated: app-20250417130026-0001/0 is now RUNNING
25/04/17 13:00:26 INFO StandaloneSchedulerBackend: SchedulerBackend is ready for scheduling beginning after reached minRegisteredResourcesRatio: 0.0
25/04/17 13:00:27 INFO SparkContext: Starting job: sum at /app/FederatedAveraging.py:30
25/04/17 13:00:27 INFO DAGScheduler: Got job 0 (sum at /app/FederatedAveraging.py:30) with 2 output partitions
25/04/17 13:00:27 INFO DAGScheduler: Final stage: ResultStage 0 (sum at /app/FederatedAveraging.py:30)
25/04/17 13:00:27 INFO DAGScheduler: Parents of final stage: List()
25/04/17 13:00:27 INFO DAGScheduler: Missing parents: List()
25/04/17 13:00:27 INFO DAGScheduler: Submitting ResultStage 0 (PythonRDD[1] at sum at /app/FederatedAveraging.py:30), which has no missing parents
25/04/17 13:00:27 INFO MemoryStore: Block broadcast_0 stored as values in memory (estimated size 7.0 KiB, free 366.3 MiB)
25/04/17 13:00:27 INFO MemoryStore: Block broadcast_0_piece0 stored as bytes in memory (estimated size 4.4 KiB, free 366.3 MiB)
25/04/17 13:00:27 INFO BlockManagerInfo: Added broadcast_0_piece0 in memory on abc55cc386c2:41229 (size: 4.4 KiB, free: 366.3 MiB)
25/04/17 13:00:27 INFO SparkContext: Created broadcast 0 from broadcast at DAGScheduler.scala:1513
25/04/17 13:00:27 INFO DAGScheduler: Submitting 2 missing tasks from ResultStage 0 (PythonRDD[1] at sum at /app/FederatedAveraging.py:30) (first 15 tasks are for partitions Vector(0, 1))
25/04/17 13:00:27 INFO TaskSchedulerImpl: Adding task set 0.0 with 2 tasks resource profile 0
25/04/17 13:00:29 INFO CoarseGrainedSchedulerBackend$DriverEndpoint: Registered executor NettyRpcEndpointRef(spark-client://Executor) (172.19.0.4:33960) with ID 1,  ResourceProfileId 0
25/04/17 13:00:29 INFO CoarseGrainedSchedulerBackend$DriverEndpoint: Registered executor NettyRpcEndpointRef(spark-client://Executor) (172.19.0.3:40040) with ID 0,  ResourceProfileId 0
25/04/17 13:00:29 INFO BlockManagerMasterEndpoint: Registering block manager 172.19.0.4:37585 with 366.3 MiB RAM, BlockManagerId(1, 172.19.0.4, 37585, None)
25/04/17 13:00:29 INFO BlockManagerMasterEndpoint: Registering block manager 172.19.0.3:37109 with 366.3 MiB RAM, BlockManagerId(0, 172.19.0.3, 37109, None)
25/04/17 13:00:29 INFO TaskSetManager: Starting task 0.0 in stage 0.0 (TID 0) (172.19.0.4, executor 1, partition 0, PROCESS_LOCAL, 4487 bytes) taskResourceAssignments Map()
25/04/17 13:00:29 INFO TaskSetManager: Starting task 1.0 in stage 0.0 (TID 1) (172.19.0.4, executor 1, partition 1, PROCESS_LOCAL, 4537 bytes) taskResourceAssignments Map()
25/04/17 13:00:29 INFO BlockManagerInfo: Added broadcast_0_piece0 in memory on 172.19.0.4:37585 (size: 4.4 KiB, free: 366.3 MiB)
25/04/17 13:00:30 INFO TaskSetManager: Finished task 0.0 in stage 0.0 (TID 0) in 1130 ms on 172.19.0.4 (executor 1) (1/2)
25/04/17 13:00:30 INFO TaskSetManager: Finished task 1.0 in stage 0.0 (TID 1) in 1100 ms on 172.19.0.4 (executor 1) (2/2)
25/04/17 13:00:30 INFO TaskSchedulerImpl: Removed TaskSet 0.0, whose tasks have all completed, from pool
25/04/17 13:00:30 INFO PythonAccumulatorV2: Connected to AccumulatorServer at host: 127.0.0.1 port: 57383
25/04/17 13:00:30 INFO DAGScheduler: ResultStage 0 (sum at /app/FederatedAveraging.py:30) finished in 2.993 s
25/04/17 13:00:30 INFO DAGScheduler: Job 0 is finished. Cancelling potential speculative or zombie tasks for this job
25/04/17 13:00:30 INFO TaskSchedulerImpl: Killing all running tasks in stage 0: Stage finished
25/04/17 13:00:30 INFO DAGScheduler: Job 0 finished: sum at /app/FederatedAveraging.py:30, took 3.055027 s
25/04/17 13:00:30 INFO SparkContext: Starting job: sum at /app/FederatedAveraging.py:31
25/04/17 13:00:30 INFO DAGScheduler: Got job 1 (sum at /app/FederatedAveraging.py:31) with 2 output partitions
25/04/17 13:00:30 INFO DAGScheduler: Final stage: ResultStage 1 (sum at /app/FederatedAveraging.py:31)
25/04/17 13:00:30 INFO DAGScheduler: Parents of final stage: List()
25/04/17 13:00:30 INFO DAGScheduler: Missing parents: List()
25/04/17 13:00:30 INFO DAGScheduler: Submitting ResultStage 1 (PythonRDD[2] at sum at /app/FederatedAveraging.py:31), which has no missing parents
25/04/17 13:00:30 INFO MemoryStore: Block broadcast_1 stored as values in memory (estimated size 7.0 KiB, free 366.3 MiB)
25/04/17 13:00:30 INFO MemoryStore: Block broadcast_1_piece0 stored as bytes in memory (estimated size 4.4 KiB, free 366.3 MiB)
25/04/17 13:00:30 INFO BlockManagerInfo: Added broadcast_1_piece0 in memory on abc55cc386c2:41229 (size: 4.4 KiB, free: 366.3 MiB)
25/04/17 13:00:30 INFO SparkContext: Created broadcast 1 from broadcast at DAGScheduler.scala:1513
25/04/17 13:00:30 INFO DAGScheduler: Submitting 2 missing tasks from ResultStage 1 (PythonRDD[2] at sum at /app/FederatedAveraging.py:31) (first 15 tasks are for partitions Vector(0, 1))
25/04/17 13:00:30 INFO TaskSchedulerImpl: Adding task set 1.0 with 2 tasks resource profile 0
25/04/17 13:00:30 INFO TaskSetManager: Starting task 0.0 in stage 1.0 (TID 2) (172.19.0.3, executor 0, partition 0, PROCESS_LOCAL, 4487 bytes) taskResourceAssignments Map()
25/04/17 13:00:30 INFO TaskSetManager: Starting task 1.0 in stage 1.0 (TID 3) (172.19.0.4, executor 1, partition 1, PROCESS_LOCAL, 4537 bytes) taskResourceAssignments Map()
25/04/17 13:00:30 INFO BlockManagerInfo: Added broadcast_1_piece0 in memory on 172.19.0.4:37585 (size: 4.4 KiB, free: 366.3 MiB)
25/04/17 13:00:30 INFO TaskSetManager: Finished task 1.0 in stage 1.0 (TID 3) in 86 ms on 172.19.0.4 (executor 1) (1/2)
25/04/17 13:00:30 INFO BlockManagerInfo: Added broadcast_1_piece0 in memory on 172.19.0.3:37109 (size: 4.4 KiB, free: 366.3 MiB)
25/04/17 13:00:31 INFO TaskSetManager: Finished task 0.0 in stage 1.0 (TID 2) in 953 ms on 172.19.0.3 (executor 0) (2/2)
25/04/17 13:00:31 INFO TaskSchedulerImpl: Removed TaskSet 1.0, whose tasks have all completed, from pool 
25/04/17 13:00:31 INFO DAGScheduler: ResultStage 1 (sum at /app/FederatedAveraging.py:31) finished in 0.966 s
25/04/17 13:00:31 INFO DAGScheduler: Job 1 is finished. Cancelling potential speculative or zombie tasks for this job
25/04/17 13:00:31 INFO TaskSchedulerImpl: Killing all running tasks in stage 1: Stage finished
25/04/17 13:00:31 INFO DAGScheduler: Job 1 finished: sum at /app/FederatedAveraging.py:31, took 0.972235 s
Initial Global Average: 41.5587
25/04/17 13:00:31 INFO SparkContext: Starting job: collect at /app/FederatedAveraging.py:39
25/04/17 13:00:31 INFO DAGScheduler: Got job 2 (collect at /app/FederatedAveraging.py:39) with 2 output partitions
25/04/17 13:00:31 INFO DAGScheduler: Final stage: ResultStage 2 (collect at /app/FederatedAveraging.py:39)
25/04/17 13:00:31 INFO DAGScheduler: Parents of final stage: List()
25/04/17 13:00:31 INFO DAGScheduler: Missing parents: List()
25/04/17 13:00:31 INFO DAGScheduler: Submitting ResultStage 2 (PythonRDD[3] at collect at /app/FederatedAveraging.py:39), which has no missing parents
25/04/17 13:00:31 INFO MemoryStore: Block broadcast_2 stored as values in memory (estimated size 5.6 KiB, free 366.3 MiB)
25/04/17 13:00:31 INFO MemoryStore: Block broadcast_2_piece0 stored as bytes in memory (estimated size 3.6 KiB, free 366.3 MiB)
25/04/17 13:00:31 INFO BlockManagerInfo: Added broadcast_2_piece0 in memory on abc55cc386c2:41229 (size: 3.6 KiB, free: 366.3 MiB)
25/04/17 13:00:31 INFO SparkContext: Created broadcast 2 from broadcast at DAGScheduler.scala:1513
25/04/17 13:00:31 INFO DAGScheduler: Submitting 2 missing tasks from ResultStage 2 (PythonRDD[3] at collect at /app/FederatedAveraging.py:39) (first 15 tasks are for partitions Vector(0, 1))25/04/17 13:00:31 INFO TaskSchedulerImpl: Adding task set 2.0 with 2 tasks resource profile 0
25/04/17 13:00:31 INFO TaskSetManager: Starting task 0.0 in stage 2.0 (TID 4) (172.19.0.4, executor 1, partition 0, PROCESS_LOCAL, 4487 bytes) taskResourceAssignments Map()
25/04/17 13:00:31 INFO TaskSetManager: Starting task 1.0 in stage 2.0 (TID 5) (172.19.0.3, executor 0, partition 1, PROCESS_LOCAL, 4537 bytes) taskResourceAssignments Map()
25/04/17 13:00:31 INFO BlockManagerInfo: Added broadcast_2_piece0 in memory on 172.19.0.4:37585 (size: 3.6 KiB, free: 366.3 MiB)
25/04/17 13:00:31 INFO BlockManagerInfo: Added broadcast_2_piece0 in memory on 172.19.0.3:37109 (size: 3.6 KiB, free: 366.3 MiB)
25/04/17 13:00:31 INFO TaskSetManager: Finished task 0.0 in stage 2.0 (TID 4) in 107 ms on 172.19.0.4 (executor 1) (1/2)
25/04/17 13:00:31 INFO TaskSetManager: Finished task 1.0 in stage 2.0 (TID 5) in 107 ms on 172.19.0.3 (executor 0) (2/2)
25/04/17 13:00:31 INFO TaskSchedulerImpl: Removed TaskSet 2.0, whose tasks have all completed, from pool
25/04/17 13:00:31 INFO DAGScheduler: ResultStage 2 (collect at /app/FederatedAveraging.py:39) finished in 0.122 s
25/04/17 13:00:31 INFO DAGScheduler: Job 2 is finished. Cancelling potential speculative or zombie tasks for this job
25/04/17 13:00:31 INFO TaskSchedulerImpl: Killing all running tasks in stage 2: Stage finished
25/04/17 13:00:31 INFO DAGScheduler: Job 2 finished: collect at /app/FederatedAveraging.py:39, took 0.127527 s
Round 1 Local Averages: [('client1', 37.88965517241379), ('client2', 41.78771929824561), ('client3', 45.06315789473684)]
Round 1 Updated Local Averages: [('client1', 37.52378930549771), ('client2', 42.244364122025395), ('client3', 44.412878378581865)]
Round 1 Global Average: 41.3937
25/04/17 13:00:31 INFO SparkContext: Starting job: collect at /app/FederatedAveraging.py:39
25/04/17 13:00:31 INFO DAGScheduler: Got job 3 (collect at /app/FederatedAveraging.py:39) with 2 output partitions
25/04/17 13:00:31 INFO DAGScheduler: Final stage: ResultStage 3 (collect at /app/FederatedAveraging.py:39)
25/04/17 13:00:31 INFO DAGScheduler: Parents of final stage: List()
25/04/17 13:00:31 INFO DAGScheduler: Missing parents: List()
25/04/17 13:00:31 INFO DAGScheduler: Submitting ResultStage 3 (PythonRDD[4] at collect at /app/FederatedAveraging.py:39), which has no missing parents
25/04/17 13:00:31 INFO MemoryStore: Block broadcast_3 stored as values in memory (estimated size 5.6 KiB, free 366.3 MiB)
25/04/17 13:00:31 INFO MemoryStore: Block broadcast_3_piece0 stored as bytes in memory (estimated size 3.6 KiB, free 366.3 MiB)
25/04/17 13:00:31 INFO BlockManagerInfo: Added broadcast_3_piece0 in memory on abc55cc386c2:41229 (size: 3.6 KiB, free: 366.3 MiB)
25/04/17 13:00:31 INFO SparkContext: Created broadcast 3 from broadcast at DAGScheduler.scala:1513
25/04/17 13:00:31 INFO DAGScheduler: Submitting 2 missing tasks from ResultStage 3 (PythonRDD[4] at collect at /app/FederatedAveraging.py:39) (first 15 tasks are for partitions Vector(0, 1))25/04/17 13:00:31 INFO TaskSchedulerImpl: Adding task set 3.0 with 2 tasks resource profile 0
25/04/17 13:00:31 INFO TaskSetManager: Starting task 0.0 in stage 3.0 (TID 6) (172.19.0.4, executor 1, partition 0, PROCESS_LOCAL, 4487 bytes) taskResourceAssignments Map()
25/04/17 13:00:31 INFO TaskSetManager: Starting task 1.0 in stage 3.0 (TID 7) (172.19.0.3, executor 0, partition 1, PROCESS_LOCAL, 4537 bytes) taskResourceAssignments Map()
25/04/17 13:00:31 INFO BlockManagerInfo: Added broadcast_3_piece0 in memory on 172.19.0.4:37585 (size: 3.6 KiB, free: 366.3 MiB)
25/04/17 13:00:31 INFO BlockManagerInfo: Added broadcast_3_piece0 in memory on 172.19.0.3:37109 (size: 3.6 KiB, free: 366.3 MiB)
25/04/17 13:00:31 INFO TaskSetManager: Finished task 0.0 in stage 3.0 (TID 6) in 89 ms on 172.19.0.4 (executor 1) (1/2)
25/04/17 13:00:31 INFO TaskSetManager: Finished task 1.0 in stage 3.0 (TID 7) in 89 ms on 172.19.0.3 (executor 0) (2/2)
25/04/17 13:00:31 INFO TaskSchedulerImpl: Removed TaskSet 3.0, whose tasks have all completed, from pool
25/04/17 13:00:31 INFO DAGScheduler: ResultStage 3 (collect at /app/FederatedAveraging.py:39) finished in 0.104 s
25/04/17 13:00:31 INFO DAGScheduler: Job 3 is finished. Cancelling potential speculative or zombie tasks for this job
25/04/17 13:00:31 INFO TaskSchedulerImpl: Killing all running tasks in stage 3: Stage finished
25/04/17 13:00:31 INFO DAGScheduler: Job 3 finished: collect at /app/FederatedAveraging.py:39, took 0.109952 s
Round 2 Local Averages: [('client1', 37.88965517241379), ('client2', 41.78771929824561), ('client3', 45.06315789473684)]
Round 2 Updated Local Averages: [('client1', 37.811200870735036), ('client2', 41.57170884482067), ('client3', 45.524221438637056)]
Round 2 Global Average: 41.6357
25/04/17 13:00:31 INFO SparkContext: Starting job: collect at /app/FederatedAveraging.py:39
25/04/17 13:00:31 INFO DAGScheduler: Got job 4 (collect at /app/FederatedAveraging.py:39) with 2 output partitions
25/04/17 13:00:31 INFO DAGScheduler: Final stage: ResultStage 4 (collect at /app/FederatedAveraging.py:39)
25/04/17 13:00:31 INFO DAGScheduler: Parents of final stage: List()
25/04/17 13:00:31 INFO DAGScheduler: Missing parents: List()
25/04/17 13:00:31 INFO DAGScheduler: Submitting ResultStage 4 (PythonRDD[5] at collect at /app/FederatedAveraging.py:39), which has no missing parents
25/04/17 13:00:31 INFO MemoryStore: Block broadcast_4 stored as values in memory (estimated size 5.6 KiB, free 366.3 MiB)
25/04/17 13:00:31 INFO MemoryStore: Block broadcast_4_piece0 stored as bytes in memory (estimated size 3.6 KiB, free 366.3 MiB)
25/04/17 13:00:31 INFO BlockManagerInfo: Added broadcast_4_piece0 in memory on abc55cc386c2:41229 (size: 3.6 KiB, free: 366.3 MiB)
25/04/17 13:00:31 INFO SparkContext: Created broadcast 4 from broadcast at DAGScheduler.scala:1513
25/04/17 13:00:31 INFO DAGScheduler: Submitting 2 missing tasks from ResultStage 4 (PythonRDD[5] at collect at /app/FederatedAveraging.py:39) (first 15 tasks are for partitions Vector(0, 1))25/04/17 13:00:31 INFO TaskSchedulerImpl: Adding task set 4.0 with 2 tasks resource profile 0
25/04/17 13:00:31 INFO TaskSetManager: Starting task 0.0 in stage 4.0 (TID 8) (172.19.0.3, executor 0, partition 0, PROCESS_LOCAL, 4487 bytes) taskResourceAssignments Map()
25/04/17 13:00:31 INFO TaskSetManager: Starting task 1.0 in stage 4.0 (TID 9) (172.19.0.4, executor 1, partition 1, PROCESS_LOCAL, 4537 bytes) taskResourceAssignments Map()
25/04/17 13:00:31 INFO BlockManagerInfo: Added broadcast_4_piece0 in memory on 172.19.0.3:37109 (size: 3.6 KiB, free: 366.3 MiB)
25/04/17 13:00:31 INFO BlockManagerInfo: Added broadcast_4_piece0 in memory on 172.19.0.4:37585 (size: 3.6 KiB, free: 366.3 MiB)
25/04/17 13:00:32 INFO TaskSetManager: Finished task 0.0 in stage 4.0 (TID 8) in 90 ms on 172.19.0.3 (executor 0) (1/2)
25/04/17 13:00:32 INFO TaskSetManager: Finished task 1.0 in stage 4.0 (TID 9) in 99 ms on 172.19.0.4 (executor 1) (2/2)
25/04/17 13:00:32 INFO TaskSchedulerImpl: Removed TaskSet 4.0, whose tasks have all completed, from pool
25/04/17 13:00:32 INFO DAGScheduler: ResultStage 4 (collect at /app/FederatedAveraging.py:39) finished in 0.112 s
25/04/17 13:00:32 INFO DAGScheduler: Job 4 is finished. Cancelling potential speculative or zombie tasks for this job
25/04/17 13:00:32 INFO TaskSchedulerImpl: Killing all running tasks in stage 4: Stage finished
25/04/17 13:00:32 INFO DAGScheduler: Job 4 finished: collect at /app/FederatedAveraging.py:39, took 0.116910 s
Round 3 Local Averages: [('client1', 37.88965517241379), ('client2', 41.78771929824561), ('client3', 45.06315789473684)]
Round 3 Updated Local Averages: [('client1', 37.07905136608449), ('client2', 42.094511636485024), ('client3', 44.850542837566564)]
Round 3 Global Average: 41.3414
25/04/17 13:00:32 INFO SparkUI: Stopped Spark web UI at http://abc55cc386c2:4040
25/04/17 13:00:32 INFO StandaloneSchedulerBackend: Shutting down all executors
25/04/17 13:00:32 INFO CoarseGrainedSchedulerBackend$DriverEndpoint: Asking each executor to shut down
25/04/17 13:00:32 INFO MapOutputTrackerMasterEndpoint: MapOutputTrackerMasterEndpoint stopped!
25/04/17 13:00:32 INFO MemoryStore: MemoryStore cleared
25/04/17 13:00:32 INFO BlockManager: BlockManager stopped
25/04/17 13:00:32 INFO BlockManagerMaster: BlockManagerMaster stopped
25/04/17 13:00:32 INFO OutputCommitCoordinator$OutputCommitCoordinatorEndpoint: OutputCommitCoordinator stopped!
25/04/17 13:00:32 INFO SparkContext: Successfully stopped SparkContext
25/04/17 13:00:33 INFO ShutdownHookManager: Shutdown hook called
25/04/17 13:00:33 INFO ShutdownHookManager: Deleting directory /tmp/spark-a31836ce-02ca-4502-8592-6297258573b5
25/04/17 13:00:33 INFO ShutdownHookManager: Deleting directory /tmp/spark-531a5fcf-4d57-45ad-92ef-f6f97585d54e
25/04/17 13:00:33 INFO ShutdownHookManager: Deleting directory /tmp/spark-a31836ce-02ca-4502-8592-6297258573b5/pyspark-e8d30f27-9b4a-42eb-b230-8ae71588d86f
```

and for proof here is a screenshot of the app actually running:

![image.png](./images/image%2011.png)

Also, here is the app in the spark UI (I ran the application twice)

![image.png](./images/image%2012.png)

We can see that the entire thing took 6 seconds.

Here are some snippets of the output that show the local, updated local and global averages in each round:

```powershell
<SNIP>
25/04/17 12:58:22 INFO DAGScheduler: Job 1 finished: sum at /app/FederatedAveraging.py:31, took 0.955745 s
Initial Global Average: 41.5587
25/04/17 12:58:22 INFO SparkContext: Starting job: collect at /app/FederatedAveraging.py:39
<SNIP>
```

```powershell
<SNIP>
25/04/17 12:58:22 INFO DAGScheduler: Job 2 finished: collect at /app/FederatedAveraging.py:39, took 0.113646 s
Round 1 Local Averages: [('client1', 37.88965517241379), ('client2', 41.78771929824561), ('client3', 45.06315789473684)]
Round 1 Updated Local Averages: [('client1', 38.50751763798023), ('client2', 42.42328889014168), ('client3', 44.39059143818749)]
Round 1 Global Average: 41.7738
25/04/17 12:58:22 INFO SparkContext: Starting job: collect at /app/FederatedAveraging.py:39
<SNIP>
```

```powershell
<SNIP>
25/04/17 12:58:22 INFO DAGScheduler: Job 3 finished: collect at /app/FederatedAveraging.py:39, took 0.110190 s
Round 2 Local Averages: [('client1', 37.88965517241379), ('client2', 41.78771929824561), ('client3', 45.06315789473684)]
Round 2 Updated Local Averages: [('client1', 38.491746215153306), ('client2', 41.469517372368266), ('client3', 44.69754662647936)]
Round 2 Global Average: 41.5529
25/04/17 12:58:22 INFO SparkContext: Starting job: collect at /app/FederatedAveraging.py:39
<<SNIP>
```

```powershell
<SNIP>
25/04/17 12:58:22 INFO DAGScheduler: Job 4 finished: collect at /app/FederatedAveraging.py:39, took 0.121733 s
Round 3 Local Averages: [('client1', 37.88965517241379), ('client2', 41.78771929824561), ('client3', 45.06315789473684)]
Round 3 Updated Local Averages: [('client1', 37.36784877957223), ('client2', 41.33775917043419), ('client3', 46.03772380238632)]
Round 3 Global Average: 41.5811
25/04/17 12:58:22 INFO SparkUI: Stopped Spark web UI at http://b24c1721988e:4040
<SNIP>
```

## Task 3

### Analyzing Hadoop:

```
 Job Counters 
                Launched map tasks=2
                Launched reduce tasks=1
                Rack-local map tasks=2
                Total time spent by all maps in occupied slots (ms)=32272
                Total time spent by all reduces in occupied slots (ms)=36408
                Total time spent by all map tasks (ms)=8068
                Total time spent by all reduce tasks (ms)=4551
                Total vcore-milliseconds taken by all map tasks=8068
                Total vcore-milliseconds taken by all reduce tasks=4551
                Total megabyte-milliseconds taken by all map tasks=33046528
                Total megabyte-milliseconds taken by all reduce tasks=37281792
```

Above is part of the logs we received when we were running our hadoop job. We can see that we have 2 map tasks and only 1 reduce task for the entire job to take place. 

`Rack-local map tasks=2` means both map tasks were executed on a node that is "rack-local," which means the task was assigned to the same physical location or rack where the data resides.

`Total time spent by all maps in occupied slots (ms) = 32272 ms` represents how long all the map tasks (across all instances) were actively utilizing the worker nodes' resources. Even if a map task takes time to complete but might be waiting on resources or completing other processes (like shuffling), the clock for "occupied slots" is still ticking as long as the task is in the worker slot.

We can see that the time in occupied slots for both tasks is relatively close with the map tasks taking slightly less time than the reduce tasks. However the actual execution time spent for each individual task is very much different. 
`Total time spent by all map tasks (ms) = 8068 ms/Total time spent by all reduce tasks (ms)=4551` This is the sum of the actual computational time spent by each individual map task, where the system is actively processing data. We can see here that the map tasks actually take twice as long as the reduce tasks. We should also keep in mind that there were two map tasks and only one reduce task in this job! So each map task would have taken less than the reduce task by itself. As our system scales, these numbers may change. It is more occurrent that map tasks take up less resources and time to complete than reduce tasks in larger jobs. 

Discuss how the job's performance might change with larger datasets or an increased number of clients: 
As the number of map tasks increases (because larger datasets require more splits), the execution time for the map phase will increase, but it should remain relatively fast as long as the data can be processed in parallel across multiple nodes in the cluster. The reduce phase will likely see a more significant increase in time as the data to be shuffled grows. Larger datasets or more clients will increase the amount of data that needs to be transferred between the map and reduce tasks. This is where the shuffle phase has a major impact on performance. If the reduce phase handles more data, it will require more time for sorting and aggregating results. The shuffle phase could become a bottleneck as the dataset grows, as it involves redistributing data across nodes. This typically involves disk and network IO, which could slow down processing if there is not enough available network bandwidth or disk space for the shuffle files.

**Consider the impact of the shuffle and reduce phases on performance:**

The shuffle process involves sorting and grouping data, which takes time and consumes both memory and disk resources. The impact of this phase is evident from the higher time spent in reduce tasks compared to map tasks. As the data size increases, the shuffle phase can become a bottleneck and may lead to longer job runtimes, especially if network or disk IO is not optimized.
The reduce phase also plays a critical role in performance. The time taken for reduce tasks (`36408 ms`) shows that this phase is where most of the computational load resides. 

Comment on the resource utilization of your Hadoop cluster during job execution:
**CPU Utilization (vcore-milliseconds)**: The total vcore-milliseconds for the map tasks (`8068`) and reduce tasks (`4551`) indicate the amount of CPU time consumed. Since the number of tasks was small (`2 map tasks, 1 reduce task`), CPU utilization seems moderate. However, with larger datasets, the number of map and reduce tasks would increase, leading to higher CPU utilization.
**Memory Utilization (megabyte-milliseconds)**: The memory used during the map tasks (`33046528 megabyte-milliseconds`) and reduce tasks (`37281792 megabyte-milliseconds`) suggests that the reduce phase is consuming more memory. The higher memory usage in the reduce phase is typical, as it deals with the final aggregation of data.
we can assume that disk and network I/O played a significant role since hadoop constantly deals with disk and is also constantly transferring data between nodes, especially during the shuffle phase. As data is shuffled between the map and reduce tasks, the network and disk performance can heavily impact job execution time. If the cluster's network bandwidth or disk throughput is insufficient, this would result in slower shuffle and reduce phases.

### Analyzing Spark:

Analyze the execution time of your Spark application:
Now the entire spark application I ran took about 6 seconds as it is visible in the Spark UI image I provided above. For Spark, the execution time depends on a variety of factors, such as the number of worker nodes, the size of the dataset, the complexity of the computations, and the resources allocated to the driver and executors. However, this spark application was running on a single worker and even if we added let’s say 100 workers, nothing would have changed. (I ran spark on client mode because in one of the repo’s discussions you said it is okay to not distribute the task on the entire cluster)

The Spark job execution:

- The application begins by initializing a SparkSession in client mode and setting up connections to the Spark master.
- In the federated averaging task, Spark first computes the local averages for each client, simulates updates to these averages, and calculates the global average at the end of each round.
- The computation of local averages and global averages occurs as parallel tasks across worker nodes. This step can take time depending on the complexity of the data (i.e., the number of clients and the number of federated learning rounds). Now I believe that even though the python script was not distributed accros all workers, the entire task was ran on a single worker node and not on the driver or the master.

**Discuss the scalability of your Spark solution, particularly in terms of handling a larger number of simulated clients and federated learning rounds:**
Spark is known for its **horizontal scalability**. This means that as the number of simulated clients and federated learning rounds increases, Spark can handle the larger workload by distributing tasks across a greater number of workers. Each round in federated learning requires calculating the global average from the local updates of each client. In Spark, the number of rounds will increase the number of iterations the algorithm runs through, but it will scale with the cluster size. More worker nodes can help process the data in each round concurrently, reducing the overall computation time.

**Compare and contrast the performance of Spark with your Hadoop implementation, highlighting the factors contributing to any observed differences:**
**Spark** generally outperforms **Hadoop MapReduce** in terms of execution time for tasks that involve iterative computation or require shuffling of data. Spark performs in-memory computation and can cache data, reducing the overhead of reading and writing from disk. This is especially beneficial in federated learning, where the task involves multiple rounds of computation. **Hadoop MapReduce** works by reading and writing data from disk at each stage of the job. This disk I/O is slower and can significantly increase the overall execution time, especially with large datasets or numerous rounds.

So to put things simply, we can say that because the task we are performing can be an example of iterative computing, Spark may be a better choice for parallelization than Hadoop and Hadoop may be more suitable for applications that require a one time batch processing of data without the reuse of that data in short periods of time. 

Both Spark and **Hadoop** are fault-tolerant. In Hadoop, fault tolerance is achieved by replicating data blocks across nodes. In Spark, fault tolerance is achieved through the use of RDDs.

**Discuss the benefits and drawbacks of using Spark and Hadoop in the context of the simulated federated learning scenario that was implemented:**

Again as I said above using Spark for this task may be a wiser choice since Spark’s in-memory computation offers faster processing than Hadoop, making it a good fit for federated learning tasks, which often involve multiple rounds of aggregation. adoop is slower than Spark due to disk I/O between the map, shuffle, and reduce phases. Federated learning, which involves multiple rounds of aggregation, would be slower on Hadoop as each round requires data to be written and read from the disk.

### **Federated Learning Challenges and Benefits**

**Challenges:**

**Data Partitioning and distributing the load:**

- In a **Federated Learning** setup, data is often distributed across multiple clients. Discuss how data partitioning might be handled in Hadoop and Spark:
    - **Hadoop**: Data partitioning is handled by HDFS (Hadoop Distributed File System). The data is split into blocks, and each block is distributed across different nodes in the cluster.
    - **Spark**: Spark handles data as RDDs (Resilient Distributed Datasets) or DataFrames, which are partitioned across the cluster.
- Challenges: Partitioning data based on the model of Federated Learning requires that each client has only access to its local data. This introduces the challenge of ensuring that models do not leak information across clients, and that data is properly partitioned and localized.

Now I don’t know about real federated learning, but it seems like distributing the load from a simple python script across a Spark cluster is quite a hassle. Unless there is an easier and better way to do it, spark may not be it😂

**Communication Overhead:**

- Federated Learning involves frequent model updates being sent between clients and a central server (in this case, the Spark master). Discuss how the communication overhead impacts both Hadoop and Spark:
    - **Hadoop**: The shuffle phase in Hadoop can lead to significant communication overhead, especially if a lot of data needs to be transferred between nodes during the reduce phase.
    - **Spark**: Spark reduces communication overhead by using in-memory computations, but still, communication between workers and the master is essential for distributed tasks.

### **Benefits**

1. **Large Dataset Handling:**
    - Hadoop and Spark both handle massive datasets efficiently. Discuss how they are used in Federated Learning to handle data from multiple clients.
2. **Distributed Computation:**
    - Both frameworks can perform parallel computations across multiple nodes, which is crucial for Federated Learning tasks that involve training models based on data from many different clients. **However, again, for the third time, Hadoop has a lot of overhead because it constantly works with disk… Bluh bluh bluh…**
