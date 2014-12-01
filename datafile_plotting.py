import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import numpy as np
import csv
import math
import Image


def plotter(plot_file, chosen_words):
    df = pd.read_csv(plot_file, encoding="utf-8",index_col='Subreddit')
    df[chosen_words].plot(kind='bar',stacked=True)#,x=df.values, y=df.columns)
    plt.xticks(rotation='0')
    plt.title('Word Frequency')
    plt.ylabel('Percentage')
    plt.savefig('testplot.png')
    Image.open('testplot.png').save('testplot.jpg','JPEG')
    plt.show()

    df['Sentiment Value'].plot(kind='bar')
    plt.xticks(rotation='0')
    plt.title('Sentiment Score')
    plt.ylabel('Word sentiment weight: N')
    plt.show()

    df['Profanity Score'].plot(kind='bar')
    plt.xticks(rotation='0')
    plt.title('Profane Words Frequency')
    plt.ylabel('Percentage')
    plt.show()

    #plt.boxplot(x=df.values)
    #plt.xticks([1, 2, 3, 4, 5, 6], df.columns)
    #plt.show()

    #df.boxplot()
    #plt.show()
    #area =[]
    #area.append(math.sqrt(df.values))
    #plt.scatter(x=df['fuck'],y=df['shit'])
    #plt.show()


# Example usage:




