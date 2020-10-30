import numpy as np
import random
import time


def cal_tardy(job_sequence, p_time, d_time, weights):
    current = 0
    total_weighted_time = 0
    for i in range(20):
        index = job_sequence[i] # receive job number for coding easily
        current += p_time[index]
        total_weighted_time += weights[index] *( max(current-d_time[index], 0) )

    return total_weighted_time

# given data
p_time={1:10,2:10,3:13,4:4,5:9,6:4,7:8,8:15,9:7,10:1,11:9,12:3,13:15,14:9,15:11,16:6,17:5,18:14,19:18,20:3}
d_time={1:50,2:38,3:49,4:12,5:20,6:105,7:73,8:45,9:6,10:64,11:15,12:6,13:92,14:43,15:78,16:21,17:15,18:50,19:150,20:99}
weights={1:10,2:5,3:1,4:5,5:10,6:1,7:5,8:10,9:5,10:1,11:5,12:10,13:10,14:5,15:1,16:10,17:5,18:5,19:1,20:5}

# start timing
start = time.time()

# initialize the job sequence
job = range(1,21,1)
job_sequence = np.random.choice(job, len(job), replace=False) # choose number randomly form the job, replace=False means that don't choose number repeatedly

min_tardy = cal_tardy(job_sequence, p_time, d_time, weights)
print(min_tardy)


iteration = 100000

for i in range(iteration):
    job_sequence = np.random.choice(job, len(job), replace=False) # choose number randomly form the job, replace=False means that don't choose number repeatedly
    tardy = cal_tardy(job_sequence, p_time, d_time, weights)
    if tardy < min_tardy:
        print('good')
        min_tardy = tardy


print()
print("total time: ", time.time() - start)
print(min_tardy)