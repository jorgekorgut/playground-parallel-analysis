import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt

import pandas as pd

import warnings
warnings.filterwarnings('ignore')


openMP = pd.read_csv('./Analysis/Part1/stats.csv',header=None,names=['version','nbcore','input','runtime'],dtype={
                     'version': str,
                     'nbcore': int,
                     'input' : str,
                     'runtime' : float
                 })

cuda = pd.read_csv('./Analysis/Cuda/stats.csv',header=None,names=['optimizationVersion','nSteps','runtime'],dtype={
                     'optimizationVersion': str,
                     'nSteps': str,
                     'runtime' : float
                 })

subplot, axis = plt.subplots(1)

input_interation_values = cuda['optimizationVersion'].unique()

colors_array = ['blue', 'red', 'yellow', 'green', 'black', 'magenta', 'cyan', 'orange', 'brown', 'black', 'black']



def plotGraph(df, title) :
    for index, input in enumerate(input_interation_values):
        df_plot = df #[df['optimizationVersion'] == key_input]
        
        mean_stats = df_plot.groupby(['optimizationVersion','nSteps']).mean().reset_index()
        mean_stats = mean_stats[mean_stats['optimizationVersion'] == input]
        axis.plot(mean_stats['nSteps'],
            mean_stats['runtime'],
        linestyle="solid",
        color=colors_array[index])

        axis.set_xlabel('number of steps')
        axis.set_ylabel('runtime (log(seconds))')
        axis.set_yscale('log')

    plt.title(title)
    plt.legend(input_interation_values)
    plt.show()

def plotKeyGraph(df, key_input) :
    for index, input in enumerate(input_interation_values):
        df_plot = [df['optimizationVersion'] == key_input]
        
        mean_stats = df_plot.groupby(['optimizationVersion','nSteps']).mean().reset_index()
        
        axis.plot(mean_stats['nSteps'],
            mean_stats['runtime'],
        linestyle="solid",
        color=colors_array[index])

        #axis.set_xlabel('nbcores (number)')
        #axis.set_ylabel('runtime (log(seconds))')
        #axis.set_yscale('log')


    # Scatter plot
    # for index, input in enumerate(input_interation_values):
    #     df_plot = df[(df['input'] == input)]
    #     df_plot = df_plot[df_plot['version'] == key_input]

    #     axis.scatter(df_plot['nbcore'], 
    #     df_plot['runtime'],
    #     color=colors_array[index])
    #     axis.set_xlabel('nbcores (number)')
    #     axis.set_ylabel('runtime (log(seconds))')
    #     axis.set_yscale('log')
    
    plt.legend(input_interation_values)
    plt.show()

def plotCompareBestOpenMPcuda() :
    bestOpenMP = openMP.groupby(['version','nbcore', 'input']).mean().reset_index()
    bestOpenMP = bestOpenMP[bestOpenMP['version'] == 'reduce']
    bestOpenMP = bestOpenMP[bestOpenMP['nbcore'] == 6].reset_index()
    bestOpenMP['input'] = bestOpenMP['input'].astype(float)

    bestCuda = cuda.groupby(['optimizationVersion','nSteps']).mean().reset_index()
    bestCuda = bestCuda[bestCuda['optimizationVersion'] == 'full-reduction']
    array = ["N:10000.0", "N:100000.0", "N:1000000.0", "N:10000000.0",  "N:100000000.0"]
    bestCuda['nSteps'] = bestCuda['nSteps'][bestCuda['nSteps'].isin(array)].str.replace("N:", "").astype(float)

    axis.plot(bestOpenMP['input'],
            bestOpenMP['runtime'],
        linestyle="solid",
        color=colors_array[0])
    
    axis.plot(bestCuda['nSteps'],
            bestCuda['runtime'],
        linestyle="solid",
        color=colors_array[1])

    axis.set_xlabel('log(number of steps)')
    axis.set_ylabel('runtime (log(seconds))')
    axis.set_yscale('log')
    axis.set_xscale('log')

    plt.legend(['OpenMP', 'Cuda'])
    plt.title("Comparaison des meilleurs temps d'execution")
    plt.show()

#plotCompare("sequential", "parallel", [input_interation_values[-1]])

#plotCompare("simd", "parallel", [input_interation_values[-1]])

#plotGraph(cuda, "Temps d'execution en fonction du nombre de pas")

plotCompareBestOpenMPcuda()