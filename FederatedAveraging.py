#!/usr/bin/env python3
from pyspark.sql import SparkSession
import random

# Initialize SparkSession in client mode
spark = SparkSession.builder \
    .appName("FederatedAveraging") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

sc = spark.sparkContext

# Option A: Read aggregated results from HDFS
# Uncomment this block if reading data
'''
lines = sc.textFile("hdfs://hdfs-namenode:9000/user/ilya/output/part-00000")
aggregated_data = lines.map(lambda line: line.strip().split()) \
                     .map(lambda parts: (parts[0], (float(parts[1]), int(parts[2]))))
''' 

# Option B: Simulate aggregated results 
aggregated_data = sc.parallelize([
    ("client1", (2197.6, 58)),
    ("client2", (2381.9, 57)),
    ("client3", (2568.6, 57))
])


# Calculate the initial global average
total_sum = aggregated_data.map(lambda x: x[1][0]).sum()
total_count = aggregated_data.map(lambda x: x[1][1]).sum()
global_avg = total_sum / total_count
print("Initial Global Average: {:.4f}".format(global_avg))

# Simulate federated averaging for 3 rounds
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
    
    # For the next round, you might choose to update your aggregated_data RDD
    # Here, we simply simulate without altering the original RDD

spark.stop()
