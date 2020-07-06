import time
import pandas as pd
import numpy as np
import json

# This code to explore US bikeshare Data

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        1. (str) city - name of the city to analyze
        2. (str) month - name of the month to filter by, or "all"
        to apply no month filter
        3. (str) day - name of the day of week to filter by, or "all"
        to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington).
    city = []
    cityFilter = ['chicago', 'new york', 'washington']
    while city not in cityFilter:
        city = input("Choose the city to analyse\n(Chicago, New York or Washington) : ").lower()

    # get user input for month (all, january, february, ... , june)
    month = []
    monthFilter = ['all','january','february','march','april', 'may','june']

    while month not in monthFilter:
        month = input("\nname of the month to filter by\n(choose from January to June, or all) : ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = []
    dayFilter = ['all', 'sunday', 'monday', 'tuesday',
                  'wednesday', 'thursday', 'friday', 'saturday']
    while day not in dayFilter:
        day = input("\nname of the day of week to filter by, or all: ").lower()

    print('-'*40, '\n')
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day
    if applicable.

    Args:
        1. (str) city - name of the city to analyze
        2. (str) month - name of the month to filter by, or "all"
        to apply no month filter
        3. (str) day - name of the day of week to filter by, or "all"
        to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print()
    print(" Filters applied :[ {}, {}, {}] ".format(city, month, day).center(78, '*'))
    print()

    # transfer data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])


    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month
    if month != 'all':

        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # based on month filter, create a new dataframe
        df = df[df['month'] == month]

    # filter by day
    if day != 'all':
        # based on day filter, create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    if 'Start Time' in df.columns:
        print('\nCalculating The Most Frequent Times of Travel...\n ')
        start_time = time.time()
        df['Start Time'] = pd.to_datetime(df['Start Time'])

        # display the most common month
        df['month'] = df['Start Time'].dt.month
        popular_month = df['month'].mode()[0]
        print('Most common Month: {}'.format(popular_month))

        # display the most common day of week
        df['day_of_week'] = df['Start Time'].dt.day_name()
        popular_day = df['day_of_week'].mode()[0]
        print('Most common day of the week: {}'.format(popular_day))

        # display the most common start hour
        df['hour'] = df['Start Time'].dt.hour
        popular_hour = df['hour'].mode()[0]
        print('Most common Start Hour: {}'.format(popular_hour))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip... \n ')
    start_time = time.time()

    # display most commonly used start station
    if 'Start Station' in df.columns:
        print('Most commonly used start station:     {} '.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    if 'End Station' in df.columns:
        print('Most commonly used End station:    {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    if 'Start Station' in df.columns and 'End Station' in df.columns:
        df['route'] = df['Start Station'] + ' -- to -- ' + df['End Station']
        print('Most frequent route:      {}'.format(df['route'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""


    if 'Trip Duration' in df.columns:
        print('\nCalculating Trip Duration... \n ')
        start_time = time.time()

        # display total travel time
        print('Total Travel Time:  {} '.format(df['Trip Duration'].sum()))

        # display mean travel time
        print('Avg Travel Time:     {} '.format(df['Trip Duration'].mean()))
        print('Most Travel Time:    {} '.format(df['Trip Duration'].mode()[0]))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats... \n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        print('User types..')
        print(df['User Type'].value_counts())
        # print()
    # Display counts of gender
    if 'Gender' in df.columns:
        print('\nGender stats..')
        df['Gender'].replace(np.nan, 'not disclosed', inplace=True)
        print(df['Gender'].value_counts(dropna=False))
        # print()
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nAge stats..')
        print('Earliest Birth Year:   {} '.format(int(df['Birth Year'].min())))
        print('Most recent Birth Year:   {} '.format(int(df['Birth Year'].max())))
        print('Most common Birth Year:   {} '.format(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)


        # Raw Data Part

        coun = 5
        rawData = input('Would you like to see raw data? Enter yes or no. \n ').lower()
        df['Start Time'] = df['Start Time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        while rawData == 'yes':
            print(json.dumps(df.head(coun).to_dict('index'), indent=1))
            rawData = input('Would you like to see more raw data? Enter yes or no. \n ').lower()
            coun += 5

        restart = input('\nWould you like to restart? Enter yes or no. \n ').lower()
        if restart.lower() != 'yes':

            print('\nThank you for using the app.\n ')
            break

if __name__ == "__main__":
    main()
