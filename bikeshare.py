import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = str(input("Please enter the city that you wish to explore(choose either Chicago, New York City, Washington or All): ").title())
        except ValueError:
            print("Sorry, you entered an invalid response. Please try again.")
            continue
        if city.title() not in ('All','Chicago', 'New York City', 'Washington') :
            print("Not an appropriate choice.")
            continue
        else:
            print("Okay, you want to filter by " + city + ", sounds great!")
            break
        # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = str(input("Please enter the month that you wish to filter by (January-June) or type 'All'  : ").title())
        except ValueError:
            print("Sorry, you entered an invalid response. Please try again.")
            continue
        if month.title() not in ('All','January', 'February', 'March' , 'April', 'May' ,'June'):
            print("Not an appropriate choice.")
            continue
        else:
            print("Okay, you want to filter by " + month + ", sounds great!")
            break

        # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = str(input("Please enter the day of the week that you wish to filter by (Monday-Sunday) or type 'All'  : ").title())
        except ValueError:
            print("Sorry, you entered an invalid response. Please try again.")
            continue
        if day.title() not in ('All','Monday', 'Tuesday', 'Wednesday' , 'Thursday', 'Friday' ,'Saturday', 'Sunday'):
            print("Not an appropriate choice.")
            continue
        else:
            print("Okay, you want to filter by " + day + ", sounds great!")
            break
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March' , 'April', 'May' ,'June']
        month_int = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month_int]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]                               
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()

    # TO DO: display the most common month 
    popular_month = df['month'].mode()[0]
    months = ['January', 'February', 'March' , 'April', 'May' ,'June']
    month_index = popular_month - 1
    print('Most Popular Month:', months[month_index])
    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Day of Week:', popular_day)
    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode().iloc[0]  
    print('Most Popular Hour:', popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Popular Start Station:', popular_start_station)
    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Popular End Station:', popular_end_station)
    # TO DO: display most frequent combination of start station and end station trip
    count_series = df.groupby(['Start Station', 'End Station']).size()
    new_df = count_series.to_frame(name = 'Count').reset_index()
    new_df.sort_values(by=['Count'], ascending=False, inplace=True)
    new_df.set_index("Count", inplace=True)
    popular_start = new_df.iloc[0]['Start Station']
    popular_end = new_df.iloc[0]['End Station']
    print('The most frequent combination of start station and end station trip is:', popular_start,' to ' , popular_end)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...')
    start_time = time.time()

    # TO DO: display total travel time (change to display as days/hours/min/sec instead of seconds)
    #total_travel = df['Trip Duration'].sum()
    #print('The total travel time is:', total_travel)

    total_travel = df['Trip Duration'].sum()
    sec = timedelta(seconds=int(total_travel))
    d = datetime(1,1,1) + sec
    print("The total travel time is \n DAYS:HOURS:MIN:SEC")
    print("%d:%d:%d:%d" % (d.day-1, d.hour, d.minute, d.second))
    
    
    # TO DO: display mean travel time
    mean_travel = df['Trip Duration'].mean()
    sec = timedelta(seconds=int(mean_travel))
    d = datetime(1,1,1) + sec
    print("The mean travel time is \n DAYS:HOURS:MIN:SEC")
    print("%d:%d:%d:%d" % (d.day-1, d.hour, d.minute, d.second))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_counts = df.groupby(['User Type']).size()
    print('The count of user types is:', user_counts)
    # TO DO: Display counts of gender  -Note Washington does not have gender in the data
    try:
        gender_counts = df.groupby(['Gender']).size()
        print('The count of gender types is:', gender_counts)
    except KeyError:
        print('Gender cannot be computed because there is a KeyError.')
        pass
        # TO DO: Display earliest, most recent, and most common year of birth - Note washington does not have birth year in the data
    try:
        birth_earliest = df['Birth Year'].min()
        print('The earliest birth year is:', birth_earliest)
    except KeyError:
        print('The earliest birth year could not be computed.')
        pass
    try:
        birth_recent = df['Birth Year'].max()
        print('The most recent birth year is:', birth_recent)
    except KeyError:
        print('The most recent birth year could not be computed')
        pass
    try:
        birth_common = df['Birth Year'].mode()
        print('The most common year of birth is:', birth_common)
    except KeyError:
        print('The most common year of birth could not be computed.')
        pass
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    #this next function asks the user if they'd like to see raw data, got help from https://stackoverflow.com/a/52938844
def more_data(df):
    st = 0
    more_data = input('\nWould you like to see the raw data? Enter yes or no.\n')
    while more_data.lower() == 'yes':
        df_slice = df.iloc[st: st+5]
        print(df_slice)
        st += 5
        more_data = input('\nWould you like to see moreeeeee data? Enter yes or   no.\n')



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        more_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
