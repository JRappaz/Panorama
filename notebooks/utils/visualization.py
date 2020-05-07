import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd

def plotTweetPerDay(df, title, rolling_window=1, vertical_line_x=None, vertical_line_label="", col_count="published", interval=2):
    # Prettier plotting with seaborn
    sns.set(font_scale=1.5, style="whitegrid")

    fig, ax = plt.subplots(figsize=(12, 8))

    # Compute rolling mean of the count if needed
    y =  df[col_count].rolling(window=rolling_window).mean()

    ax.plot(df['date'],
           y,
            '-o',
            color='purple', marker="")
    ax.set(xlabel="Date", ylabel="# Tweets",
           title=title)

    # Plot the vertical line if needed
    if vertical_line_x is not None:
        plt.axvline(linewidth=4, color='r', x=vertical_line_x, label=vertical_line_label)
    
    # Format the x axis
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=interval))
    ax.xaxis.set_major_formatter(DateFormatter("%d-%m-%y"))

    # Ensure ticks fall once every other week (interval=2) 
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=interval))
    plt.legend()
    plt.show()

def plotTweetPerDay2Axis(df, y_1_col, y_2_col, x, y_1_label="", y_2_label="", vertical_line_x=None, vertical_line_label=""):
    # Prettier plotting with seaborn
    sns.set(font_scale=1.5, style="whitegrid")

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(df[x],
            df[y_1_col].rolling(window=1).mean(),
            '-o',
            color='purple', label="medias")
    ax.set_ylabel(y_1_label, color='purple')
    ax.tick_params(axis='y', labelcolor='purple')
    ax.set(xlabel="Date",
           title="Number of tweets send by users or medias on Coronavirus per day")

    ax2 = ax.twinx()
    ax2.plot(df[x],
            df[y_2_col].rolling(window=1).mean(),
            '-o',
            color='blue', label="users")
    ax2.set_ylabel(y_2_label, color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')

    if vertical_line_x is not None:
        plt.axvline(linewidth=4, color='r', x=vertical_line_x, label=vertical_line_label)

    # Format the x axis
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    ax.xaxis.set_major_formatter(DateFormatter("%d-%m-%y"))

    # Ensure ticks fall once every other week (interval=2) 
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    #plt.legend()
    plt.show()
