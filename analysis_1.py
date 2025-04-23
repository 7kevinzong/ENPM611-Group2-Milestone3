from typing import List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.dates as mdates

from data_loader import DataLoader
from model import Issue,Event
import config



class Analysis1:
    """
    Implements an example analysis of GitHub
    issues and outputs the result of that analysis.
    """
    
    def __init__(self):
        # load dataset based off config
        self.DATASET:str = config.get_parameter('dataset')
        if self.DATASET == None:
            self.DATASET = 0
        
        # select all issues or one user
        self.USER:str = config.get_parameter('user')
        
        
    def run(self):
        print("Started analysis 1")
        
        # load issues
        issues:List[Issue] = DataLoader(self.DATASET).get_issues()
        
        # Create a dataframe (with only the creator's name) to make statistics a lot easier
        df = pd.DataFrame.from_records([{'creator':issue.creator, 'date created':issue.created_date} for issue in issues])
        
        # if a user is specified, only select dates for that user
        if self.USER is not None:
            print(f"Showing trends for user {self.USER}")
            df = df[df['creator'] == self.USER]
        
        # get dates from dataframe
        dates = df['date created']
        
        # Convert to matplotlib date numbers
        date_nums = mdates.date2num(dates)

        # Define number of bins (e.g., weekly, monthly, etc.)
        counts, bin_edges = np.histogram(date_nums, bins=20)

        # Find midpoints of each bin for plotting
        bin_midpoints = 0.5 * (bin_edges[1:] + bin_edges[:-1])


        # set the seaborn theme
        sns.set_theme()
        
        # Plot the trend line
        plt.plot(bin_midpoints, counts, marker=None)
        

        # Format the x-axis with readable dates
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gcf().autofmt_xdate()
        
        # plot the sorted data on a timeline
        plt.xlabel("Date")
        plt.ylabel("Number of Issues Created")
        plt.title("Issue Trend Over Time")
        plt.grid(True)
        plt.show()
        
        # plt.hist(dates, bins=30)
        # plt.title("Number of Issues Created by Year")
        # plt.xlabel("Year")
        # plt.ylabel("# of issues")
        # plt.show()
        

if __name__ == "__main__":
    Analysis1().run()