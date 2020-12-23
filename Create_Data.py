import pandas as pd
import numpy as np
import random
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
"""
# set up for genetic algorithm
noDays = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
populationsize = 5
tournamentSize = 2
probabilityGeneSwap = 0.5
mutationRate = 0.05
""" Temperature """
for i in range(1): # itarate through each month
    # create population
    population = np.random.uniform(lowT[i], highT[i],(populationsize,noDays[i]))

    # Calculate Fitness of individuals in population
    fitness = fitnessFunc(population, avgT[i])
    print(fitness)
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
        print(fitness)
        # Has mean been found? If so break out of while loop
        findZero = np.where(fitness <= 0.0001)
        if len(findZero[0]) > 0:
            break


    # pull out data that matches correct mean and save to
    print('end fitness', fitness)
    print('avg mean', avgT[0])
    print(population[np.where(fitness == min(fitness))])
    print('calc mean', population[np.where(fitness == min(fitness))].mean())

