import time
import pandas as pd
import numpy as np
import json

city_data = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

month_data = [ 'january',
               'february',
               'march',
               'april',
               'may',
               'june',
               'all']

day_data = [ 'monday',
             'tuesday',
             'wednesday',
             'thursday',
             'friday',
             'saturday',
             'sunday',
             'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    city_input = ''
    while city_input.lower() not in city_data.keys():
        city_input = input('Choose a city. Would you like to see data for \'Chicago\', \'New York\' or \'Washington\'?\n').lower()
        if city_input.lower() == 'chicago':
            city = 'chicago'
        elif city_input.lower() == 'new york':
            city = 'new york'
        elif city_input.lower() == 'washington':
            city = 'washington'
        else:
            print('Sorry, it seems your input was incorrect. Please input either Chicago, New York or Washington\n')

    print("Good choice! We´ll continue with city {}".format(city.title()))

    # get user input for month (all, january, february, ... , june)
    month_input = ''

    while month_input.lower() not in month_data:
        month_input = input('Which month do you want to display? January, February, March, April, May, June or All?\n')
        if month_input.lower() in month_data:
            month = month_input.lower()
            print("You selected to analyze data for {}".format(month.title()))
        else:
            print('Sorry, your input is incorrect. Please type in a month between January and June or All\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_input = ''


    while day_input.lower() not in day_data:
        day_input = input('Which day do you want to display? Choose between Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All\n')
        if day_input.lower() in day_data:
            day = day_input.lower()
            print("You selected to analyze data for {}".format(day.title()))
        else:
            print('Sorry, your input is incorrect. Please type in a day between Monday and Sunday or All')

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
    # load the city data file into the dataframe
    df = pd.read_csv(city_data[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day and hour from Start Time and create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter data by month
    if month != 'all':
        month = month_data.index(month) + 1
        df = df[ df['month'] == month ]

    # filter data by day
    if day != 'all':
       df = df[ df['day_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].value_counts().idxmax()
    print("The most common month is:", most_common_month)

    # display the most common day of week
    most_common_weekday = df['day_week'].value_counts().idxmax()
    print("The most common day of week is:", most_common_weekday)

    # display the most common start hour
    most_common_start_hour = df['hour'].value_counts().idxmax()
    print("The most common start hour is:", most_common_start_hour, "o´clock")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()


    # display most commonly used start station
    most_used_start_station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station is:", most_used_start_station)

    # display most commonly used end station
    most_used_end_station = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station is:", most_used_end_station)

    # display most frequent combination of start station and end station trip
    most_frequent_combination_stations = df[['Start Station', 'End Station']].mode().loc[0]
    print("The most frequent combination is Start Station: {} and End Station: {}".format(most_frequent_combination_stations[0], most_frequent_combination_stations[1]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    ttravel_time = df['Trip Duration'].sum()
    print("The total travel time is:", ttravel_time)

    # display mean travel time
    mtravel_time = df['Trip Duration'].mean()
    print("The average travel time is:", mtravel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Count of user types:")
    count_users = df['User Type'].value_counts()
    for user, count_user in enumerate(count_users):
        print("{}: {}".format(count_users.index[user], count_user))

    print(' '*40)

    # Display count of genders
    if 'Gender' in df.columns:
        print("Counts of gender:")
        count_genders = df['Gender'].value_counts()
        for gender, count_gender in enumerate(count_genders):
            print("{}: {}".format(count_genders.index[gender], count_gender))

    print(' '*40)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        birth_year = df['Birth Year']

    # display earliest birth year
    if 'Birth Year' in df.columns:
        earliest_by = birth_year.min()
        print("The earliest birth year is:", int(earliest_by))

    # display most recent birth year
    if 'Birth Year' in df.columns:
        most_recent_by = birth_year.max()
        print("The most recent birth year is:", int(most_recent_by))

    # most common birth year
    if 'Birth Year' in df.columns:
        most_common_by = birth_year.value_counts().idxmax()
        print("The most common birth year is:", int(most_common_by))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Display the raw bikeshare data"""

    row_length = df.shape[0]

    # iterate from 0 to the number of rows in steps of 5
    for i in range(0, row_length, 5):

        user_input = input('\nWould you like to display raw user trip data? Type any key or no.\n> ')
        if user_input.lower() == 'no':
            break

        # retrieve and convert data into json format
        # split json row data
        row_data = df.iloc[i: i + 5].to_json(orient='records', lines=True).split('\n')
        for row in row_data:
            # print user data
            row_parsed = json.loads(row)
            row_json = json.dumps(row_parsed, indent=2)
            print(row_json)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
