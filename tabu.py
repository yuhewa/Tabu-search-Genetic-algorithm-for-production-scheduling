import numpy as np
import random
import time


class tabu_search():
    def __init__(self,p_time,d_time,weights,job_sequence):
        self.p_time = p_time
        self.d_time = d_time
        self.weights = weights
        self.job_sequence= job_sequence

        # variant for tabu list
        self.tabu_list = []
        self.oldest_tabu_index = 0

    def cal_tardy(self):
        current = 0
        total_weighted_time = 0
        for i in range(20):
            index = self.job_sequence[i] # receive job number for coding easily
            current += self.p_time[index]
            total_weighted_time += self.weights[index] *( max(current-self.d_time[index], 0) )
        # print("Total Weighted Time: ",total_weighted_time)
        return total_weighted_time
    

    def search(self, tabu_size):
        min_tardy = self.cal_tardy()
        current_tardy = min_tardy

        # traversal all the pairs
        for i in range(19):

            # search the tubu list to determine if (i,i+1) is in the tabu list
            in_tabu = False
            for j in range(len(self.tabu_list)):
                if (i,i+1) == self.tabu_list[j]:
                    in_tabu = True
                    break

            # calculate neighborhood tardiness
            if (not in_tabu):
                # swap the neighbor and calculate tardiness then swap again to back to the original list
                self.job_sequence[i], self.job_sequence[i+1] = self.job_sequence[i+1], self.job_sequence[i]
                current_tardy = self.cal_tardy()
                temp_tabu = (i,i+1)
                self.job_sequence[i], self.job_sequence[i+1] = self.job_sequence[i+1], self.job_sequence[i]
                # record the minimal tardiness and its neighbor pair
                if (min_tardy >= current_tardy):
                    min_tardy = current_tardy
                    temp_tabu = (i,i+1)
                
        # update the tabu list
        if ( len(self.tabu_list) < tabu_size ):
            self.tabu_list.append(temp_tabu)
        else:
            self.tabu_list[self.oldest_tabu_index] = temp_tabu
            self.oldest_tabu_index = (self.oldest_tabu_index + 1) % tabu_size

        # updata the job sequence (determined by minimal tardiness)
        self.job_sequence[temp_tabu[0]], self.job_sequence[temp_tabu[1]] = self.job_sequence[temp_tabu[1]], self.job_sequence[temp_tabu[0]]

        # print("minimal tardiness: ",min_tardy)
        # print("tabu list: ",self.tabu_list)
        return min_tardy



# given data
p_time={1:10,2:10,3:13,4:4,5:9,6:4,7:8,8:15,9:7,10:1,11:9,12:3,13:15,14:9,15:11,16:6,17:5,18:14,19:18,20:3}
d_time={1:50,2:38,3:49,4:12,5:20,6:105,7:73,8:45,9:6,10:64,11:15,12:6,13:92,14:43,15:78,16:21,17:15,18:50,19:150,20:99}
weights={1:10,2:5,3:1,4:5,5:10,6:1,7:5,8:10,9:5,10:1,11:5,12:10,13:10,14:5,15:1,16:10,17:5,18:5,19:1,20:5}

# start timing
start = time.time()

# initialize the job sequence
job = range(1,21,1)
job_sequence = np.random.choice(job, len(job), replace=False) # choose number randomly form the job, replace=False means that don't choose number repeatedly

# setting the hyperparameter
iteration = 100
tabu_size = 4

tabu = tabu_search(p_time, d_time, weights, job_sequence)
print ("current minimal tardy: {}".format(tabu.cal_tardy()))

history_min_tardy = np.zeros(iteration, dtype=np.int)

for i in range(iteration):
    # print("-------------------------------------------------")
    # print('iteration: ',i)
    history_min_tardy[i] = tabu.search(tabu_size)



print("##############  after search #################################")

print("minimal tardiness: ",history_min_tardy.min())
# print("best job sequence:")
# print(tabu.job_sequence)
print("total time: ", time.time() - start)
print()
print("################################################")
print()



# following code just for test.
# test_list = [(1,2),(3,4),(5,6)]
# print(test_list[0])
# for i in range(20):
#     in_tabu = False
#     for j in range(len(test_list)):
#         if (i,i+1) == test_list[j]:
#             in_tabu = True
#             break
#     if (not in_tabu):
#         pass

