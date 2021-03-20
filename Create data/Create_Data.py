import pandas as pd
import numpy as np
import random
import pandas as pd
from datetime import datetime

def fitnessFunc(population, target):
    result = abs(population.mean(1) - target)
    return result

""" 
Import and organise data
"""
""" Temperature """
temperature_data = pd.read_csv('Temperature data.csv')

# Place high, average and low temperatures in to variables
highT, avgT, lowT = temperature_data['High C'], temperature_data['Average C'], temperature_data['Low C']

"""
Create random temperature distribution for each month based on the specific high and low temperature values around its
mean. 

This uses a genetic algorithm to find random values with the correct mean value for that month

hourly data is then created for each daily mean. This is then organised to create the riseing and fall of the 
temperatures through the night and day. This is done by placing the top temperature randomly between 12 and 3pm then 
randomly placing the 2nd and 3rd highest randomly on each side of the peak. The rest of the data is then sorted from low 
to high on the left side and high to low on the right side. 
"""
# set up for genetic algorithm for daily means
noDays = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])  # number of days in each month
dayMeans = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}  # key is month number,
                                                                                       # value = day means
populationsize = 20
tournamentSize = 2
probabilityGeneSwap = 0.5
mutationRate = 0.05

""" Temperature """
# Create daily mean values
for i in range(len(noDays)): # itarate through each month
    # create population
    population = np.random.uniform(lowT[i], highT[i],(populationsize,noDays[i]))

    # Calculate Fitness of individuals in population
    fitness = fitnessFunc(population, avgT[i])
    best_selection = population[np.where(fitness == min(fitness))]

    # iterate through generations until required mean is met
    while True:
        # select competitors
        competitorsIndex = np.array(random.sample(range(len(population)), tournamentSize))
        competitorsFitness = fitness[list(competitorsIndex)]

        # index of fittest and lowest value
        highest, lowest = np.where(fitness == max(competitorsFitness)), np.where(fitness == min(competitorsFitness))
        winner, loser = lowest[0][0], highest[0][0]

        # assign genes to loser with possibility and mutation
        for g in range(noDays[i]):
            if random.random() < probabilityGeneSwap:
                population[loser, g] = population[winner, g]

            if random.random() < mutationRate:
                population[loser, g] = random.uniform(lowT[i], highT[i])

        # Recalculate fitness's
        fitness = fitnessFunc(population, avgT[i])

        # Has mean been found? If so break out of while loop
        findZero = np.where(fitness <= 0.0001)
        if len(findZero[0]) > 0:
            break


    # pull out data that matches correct mean and save to
    month_data = population[np.where(fitness == min(fitness))]
    dayMeans[i] = month_data

# create hourly data for each daily mean. This is then organised to create the riseing and fall of the temperatures
# through the night and day. This is done by placing the top temperature randomly between 12 and 3pm then randomly
# placing the 2nd and 3rd highest randomly on each side of the peak. The rest of the data is then sorted from low to
# high on the left side and high to low on the right side.

# Create hourly mean values
hourlyValues = np.zeros([365, 24]) # number of hours in year
h = 0 
# select month
for i in range(len(dayMeans)):  
    monthData = dayMeans.get(i)
    # select day mean
    for g in range(len(monthData[0])):
        #print('day', monthData[0][g])
        # create population
        population = np.random.uniform(lowT[i], highT[i],(populationsize, 24))

        # Calculate Fitness of individuals in population
        fitness = fitnessFunc(population, monthData[0][g])
        best_selection = population[np.where(fitness == min(fitness))]

        # iterate through generations until required mean is met
        while True:
            # select competitors
            competitorsIndex = np.array(random.sample(range(len(population)), tournamentSize))
            competitorsFitness = fitness[list(competitorsIndex)]

            # index of fittest and lowest value
            highest, lowest = np.where(fitness == max(competitorsFitness)), np.where(fitness == min(competitorsFitness))
            winner, loser = lowest[0][0], highest[0][0]

            # assign genes to loser with possibility and mutation
            for j in range(24):
                if random.random() < probabilityGeneSwap:
                    population[loser, j] = population[winner, j]
 
                if random.random() < mutationRate:
                    population[loser, j] = random.uniform(lowT[i], highT[i])

            # Recalculate fitness's
            fitness = fitnessFunc(population, monthData[0][g])

            # Has mean been found? If so break out of while loop
            findZero = np.where(fitness <= 0.01)
            print('best fitness', min(fitness))
            print('h', h)
            if len(findZero[0]) > 0:
                break
        
        # pull out data that matches correct mean and save to
        day_data = population[np.where(fitness == min(fitness))][0]

        # organise data for time of day then place in hourlyValues matrix
        day_data.sort()
        b = np.zeros(24)
        choseMaxhour = random.randint(12, 14)
        b[choseMaxhour] = day_data[-1]

        placer = 1
        while len(day_data) > 0:
            day_data = np.delete(day_data, -1)
            while choseMaxhour + placer <= 23:
                b[choseMaxhour + placer] = day_data[-1]
                day_data = np.delete(day_data, -1)
                b[choseMaxhour - placer] = day_data[-1]
                placer += 1
            lenLeft = len(day_data)
            b[0:lenLeft] = day_data
        
        hourlyValues[h] = b
        h += 1
        
#print('hourly values', hourlyValues)

"""
Export data to CSV 
"""
df = pd.DataFrame(hourlyValues, columns=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
df.to_csv(r'HourlyTemperature.csv')      

