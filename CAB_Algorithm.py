#CAB Algorithm from the "On Continuum Armed Bandit Problems in High Dimensions" paper
#@Berk Tınaz
#@Last Edited May 16, 2018

import math
import numpy as np
from operator import add
import matplotlib

def CAB( d, k):
    T = 2 #given T = 1 in the original text but T = 1 makes "M" undefined so it is taken as 2.

    #Family of Partitions = A

    #Generate A
    D = [i for i in range(1,d+1)]
    A = list(k_partitions( D, k)) #A = partitions
    n = 100 #number of rounds
    a = 0.2 #element of (0,1)

    while T <= n:
        #debug
        print("Round: " + str(T))

        #calculate M
        temp1 = k ** ((a - 3) / 2)
        temp2 = math.exp( -k / 2)
        temp3 = math.log(d) ** (-0.5)
        temp4 = math.sqrt(T /(math.log10(T)))
        M = math.ceil((temp1 * temp2 * temp3 * temp4) ** (2 / (2*a + k))) #ceil the number
        #M = 3
        print(M)

        #generate XAj vectors using A
        basis =[]

        for partitions in A:
            basis_vectors = []
            for set in partitions:
                temp = [0 for i in range(d)]
                for elements in set:
                    temp[int(elements)-1] = 1
                basis_vectors.append(temp)
            basis.append(basis_vectors)

        #debug
        print("Basis:")
        for i in basis:
            print(i)
        print("***********************************************")

        #Pm generator
        sum = []
        for bsis in basis:
            temp_sum = []
            for temp in bsis:
                for i in range(1,M+1):
                    temp_sum.append([i*t for t in temp])

            #linear combination of basis
            sumt = [np.array(temp_sum[i]) for i in range(M)]
            for t in range(1,k):
                sum_temp = []
                sumtt = [temp_sum[i] for i in range(t*M,(t+1)*M)]
                for i in range(len(sumt)):
                    for j in range(M):
                        x = np.array(sumt[i])
                        y = np.array(sumtt[j])
                        sum_temp.append(x+y)
                sumt = [i for i in sum_temp]

            for i in sumt:
                i = i.tolist()
                if i not in sum:
                    sum.append([t/M for t in i])

        #debug
        print("PM:")
        for i in sum:
            print(i)
        print("********************************************")

        #Initialize MAB
        machine_averages = [reward_function(i) for i in sum]

        machine_play_amount = [1 for i in range(len(sum))]
        max_array = [0 for i in range(len(sum))]
        max_index = 0 #by default

        #start looping
        for t in range(T, min(2*T-1, n)+1):

            #find the machine maximizing
            for i in range(len(sum)):
                max_array[i] = machine_averages[i] + math.sqrt(2*math.log(n)/machine_play_amount[i])

            #get max index
            max_index = max_array.index(max(max_array))

            #get reward of corresponding index
            reward = reward_function(sum[max_index])
            print("Reward: " + str(reward))

            #update averages and play amount
            machine_sum_temp = machine_averages[max_index] * machine_play_amount[max_index]
            machine_play_amount[max_index] += 1
            machine_averages[max_index] = (machine_sum_temp + reward) / machine_play_amount[max_index]

        T = 2*T
        print("**************************************************")
        #Final results
        print("Machine Averages:")
        for i in machine_averages:
            print(i)
        print("**************************************************")

        print("Machine Play Amounts:")
        for i in machine_play_amount:
            print(i)
        print("**************************************************")

    return



def k_partitions(seq, k):

    n = len(seq)
    groups = []  # a list of lists, currently empty

    def generate_partitions(i):
        if i >= n:
            yield list(map(tuple, groups)) #list of group tuples
        else:
            if n - i > k - len(groups): #ensure remaining elements is enough to generate k subsets
                for group in groups:
                    group.append(seq[i]) #add to current sublists
                    yield from generate_partitions(i + 1) #generate it's own subgroup
                    group.pop()

            if len(groups) < k: #make sure length is k
                groups.append([seq[i]])
                yield from generate_partitions(i + 1)
                groups.pop()

    return generate_partitions(0)

def reward_function(i, n):
    sum = 0
    for x in i:
        sum = sum - x**3 + 5*x**2 - 6*x + 19
    return sum


#testing
CAB(10,1)
