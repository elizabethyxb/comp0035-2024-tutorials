from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def draw_histogram(df, columns):
    ### hello
     # Create a histogram of the DataFrame
    df[columns].hist()

    # Show the plot
    plt.show()

def draw_boxplot(df):
    
    df.plot.box(subplots=True, sharey=False)
    #subplots=True, sharey=False

    #plt.savefig('bp_example.png')
    plt.show()

def draw_timeseries(df,date_column, value_column, filter_value):
    
    #ACTIVITY 3.4 NOT WORKING AS EXPECTED
    # Sort the DataFrame by the date column
    df = df.sort_values(by=date_column)

    #df.plot(x=date_column, y=value_column)

    #df.groupby("type").plot(x=date_column, y=value_column)

    #Tutor Solution
    #df.plot(x='start', y='participants')
    #if filter_value:
    #    df = df[df['column_name'] == filter_value]

    # Group the DataFrame by the type column (winter/summer)
    # This still displays all the data though so there is a dip in the line
    # df.groupby("type").plot(x=date_column, y=value_column)
    # df.plot(x=date_column, y=value_column)

    # This version draws one line for each 'type'
    #df_summer = df[df['type'] == 'summer']
    #df_winter = df[df['type'] == 'winter']
    #ax = df_summer.plot(x=date_column, y=value_column, label='Summer games')
    #df_winter.plot(x=date_column, y=value_column, ax=ax, label='Winter games')
    #plt.xticks(rotation=90) """

    # Split by male and female
#    df_female = df[df['gender'] =='Female']
#    df_male = df[df['gender'] == 'Male']

    
    ax = df[df['type']=='summer'].plot(x=date_column, y='participants_f', label= 'Female')
    df[df['type']=='summer'].plot(x=date_column, y='participants_m', ax=ax, label='Male')


    plt.show()

if __name__ == '__main__':
    project_root = Path(__file__).parent.parent

    # Find the .csv file relative to the project root and join to that path the data folder and then the example.csv file
    prepared_file = project_root.joinpath('tutorialpkg', 'data', 'paralympics_events_prepared.csv')
    # csv_file = project_root / 'data' / 'example.csv' # this notation would also work, even though you think the '/' is only unix/macOS

    dfprepared = pd.read_csv(prepared_file)

    summer_df = dfprepared[dfprepared['type'] == 'summer']
    #print(dfprepared.head())
    draw_timeseries(dfprepared, 'start', 'participants', False)

