import numpy as np
import random
import time



class gene_search():
    def __init__(self,p_time,d_time,weights,job,genome_size,offspring_size):
        self.p_time = p_time
        self.d_time = d_time
        self.weights = weights

        self.genome_size = genome_size
        self.offspring_size = offspring_size

        
        # the first generation
        self.job_sequence = np.zeros((genome_size,20), dtype=np.int)
        for i in range(genome_size):
            self.job_sequence[i] = np.random.choice(job, len(job), replace=False) # choose number randomly form the job, replace=False means that don't choose number repeatedly
    
        # initialize offspring
        self.new_job_sequence = np.zeros((offspring_size,20), dtype=np.int)


    def cal_tardy(self, offspring = False):
        if offspring == True:
            job_sequence = self.new_job_sequence
        else:
            job_sequence = self.job_sequence


        weighted_tardy_time = np.zeros(len(job_sequence))

        for j in range( len(job_sequence) ):
            current_time = 0
            for i in range(20):
                index = job_sequence[j][i] # receive job number for coding easily
                current_time += self.p_time[index]
                weighted_tardy_time[j] += self.weights[index] *( max(current_time - self.d_time[index], 0) )
            
            # print("genome ",j," Weighted Time: ",weighted_tardy_time[j])
            
        return weighted_tardy_time


    def crossover(self):
        for i in range(0, self.offspring_size, 2):
            # decide which two genomes crossover
            genome_num =  np.random.choice(self.genome_size, 2, replace=False) 
            genome_1 = genome_num[0]
            genome_2 = genome_num[1]

            self.new_job_sequence[i], self.new_job_sequence[i+1] = self.job_sequence[genome_1], self.job_sequence[genome_2]
            

            interested_job = np.arange(1,10+1,dtype=np.int)
            
            interested_job_order_1 = []
            interested_job_order_2 = []

            mpa_order_1 = {}
            mpa_order_2 = {}
            for j in range(20):
                if self.job_sequence[genome_1][j] in interested_job:
                    interested_job_order_1.append(self.job_sequence[genome_1][j])
                if self.job_sequence[genome_2][j] in interested_job:
                    interested_job_order_2.append(self.job_sequence[genome_2][j])
            
            for j in range(10):
                mpa_order_1[interested_job_order_1[j]] = interested_job_order_2[j]
                mpa_order_2[interested_job_order_2[j]] = interested_job_order_1[j]

            for j in range(20):    
                index = self.new_job_sequence[i][j]   
                if index in interested_job:
                    self.new_job_sequence[i][j] = mpa_order_1[index]
            
            for j in range(20):    
                index = self.new_job_sequence[i+1][j]   
                if index in interested_job:
                    self.new_job_sequence[i+1][j] = mpa_order_2[index]


            
    def mutation(self, probability):
        x = random.random()
        if x < probability:
            # decide which one genomes mutate
            genome_num =  np.random.choice(self.offspring_size, 1, replace=False)[0]
            # decide the site
            mutation_site = np.random.randint(low=1, high=18, size=1)[0]
            # mutation means swap site and its next
            self.new_job_sequence[genome_num][mutation_site], self.new_job_sequence[genome_num][mutation_site+1] = self.new_job_sequence[genome_num][mutation_site+1], self.new_job_sequence[genome_num][mutation_site]       
    
    # last work here
    def evaluation(self):
        score = np.zeros(self.offspring_size, dtype=np.float)
        
        # make piechart for tardy
        tardy = self.cal_tardy(offspring=True)
        
        for i in range(self.offspring_size):
            score[i] = 1 / tardy[i]
        score = score / score.sum()

        for i in range(1, self.offspring_size):
            score[i] = score[i] + score[i-1]


        # determine offspring by its score
        # current problem: tardy and score is Proportional, make no sence
        choosed_offspring = np.zeros(genome_size, dtype=np.int)
        current_choosed_size = 0

        while ( current_choosed_size < genome_size ):
            probability = random.random()
            i = 0
            while (i < offspring_size):
                if (probability < score[i]) and (not i in choosed_offspring):
                    choosed_offspring[ current_choosed_size ] = i
                    current_choosed_size += 1
                    break
                else:
                    i += 1        


        for i in range(genome_size):
            new_job_number = choosed_offspring[i]
            self.job_sequence[i] = self.new_job_sequence[new_job_number]



# given data
p_time={1:10,2:10,3:13,4:4,5:9,6:4,7:8,8:15,9:7,10:1,11:9,12:3,13:15,14:9,15:11,16:6,17:5,18:14,19:18,20:3}
d_time={1:50,2:38,3:49,4:12,5:20,6:105,7:73,8:45,9:6,10:64,11:15,12:6,13:92,14:43,15:78,16:21,17:15,18:50,19:150,20:99}
weights={1:10,2:5,3:1,4:5,5:10,6:1,7:5,8:10,9:5,10:1,11:5,12:10,13:10,14:5,15:1,16:10,17:5,18:5,19:1,20:5}

# start timing
start = time.time()

# initialize the job sequence
job = range(1,21,1)


# setting the hyperparameter
iteration = 300
genome_size = 35
offspring_size = genome_size*2
mutation_probability = 0.01


gene = gene_search(p_time, d_time, weights, job, genome_size, offspring_size)


gene.crossover()

print ("current minimal tardy: {}".format(gene.cal_tardy(offspring=False).min() ))

history_min_tardy = np.zeros(iteration, dtype=np.int)

for i in range(iteration):
    gene.crossover()
    gene.mutation(mutation_probability)
    gene.evaluation()
    history_min_tardy[i] = gene.cal_tardy(offspring=False).min()

 

print("##############  after search #################################")

print("minimal tardiness: ",history_min_tardy.min())
# print("best job sequence:")
print("total time: ", time.time() - start)
print()
print("################################################")