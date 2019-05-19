import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        # initialize variables
        city = str()
        month = str()
        day = str()

        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        valid_city = ['chicago', 'chic', 'ch', 'c', 'new york city', 'new york', 'nyc', 'ny', 'n', 'washington', 'wash', 'wa', 'w']
        while (city.lower() not in valid_city):
            city = input('Enter a city (Chicago, New York City, or Washington): ')
            if (city.lower() not in valid_city):
                print('Sorry. That is an invalid entry. Please try again.')
        # reassign city
        if city in ['chic', 'ch', 'c']:
            city = 'chicago'
        elif city in ['new york', 'nyc', 'ny', 'n']:
            city = 'new york city'
        elif city in ['wash', 'wa', 'w']:
            city = 'washington'


        # get user input for month (all, january, february, ... , june)
        valid_month = ['all', 'january', 'jan', 'february', 'feb', 'march', 'mar', 'april', 'apr', 'may', 'june', 'jun']
        while (month.lower() not in valid_month):
            month = input('Enter a month (January through June) to filter, or enter all: ')
            if (month.lower() not in valid_month):
                print('Sorry. That is an invalid entry. Please try again.')
        # reassign month
        month_dict = {'jan': 'january', 'feb': 'february', 'mar': 'march', 'apr': 'april', 'may': 'may', 'jun':'june'}
        if month in month_dict:
            month = month_dict[month]


        # get user input for day of week (all, monday, tuesday, ... sunday)
        valid_day = ['all', 'monday', 'mon', 'mo', 'm', 'tuesday', 'tues', 'tue', 'tu', 'wednesday', 'wed', 'we', 'w', 'thursday', 'thurs', 'th', 'friday', 'fri', 'fr', 'f', 'saturday', 'sat', 'sa', 'sunday', 'sun', 'su']
        while day not in valid_day:
            day = input('Enter a day (Monday through Sunday) to filter, or enter all: ')
            if (day.lower() not in valid_day):
                print('Sorry. That is an invalid entry. Please try again.')
        # reassign day
        if day in ['mon', 'mo', 'm']:
            day = 'monday'
        elif day in ['tues', 'tue', 'tu']:
            day = 'tuesday'
        elif day in ['wed', 'we', 'w']:
            day = 'wednesday'
        elif day in ['thurs', 'th']:
            day = 'thursday'
        elif day in ['fri', 'fr', 'f']:
            day = 'friday'
        elif day in ['sat', 'sa']:
            day = 'saturday'
        elif day in ['sun', 'su']:
            day = 'sunday'

        # output the user selected information and prompt user to verify everything is correct
        print('\n\nYour Selected City: {}\nYour Selected Month: {}\nYour Selected Day: {}'.format(city.title(), month.title(), day.title()))
        correct = str()
        valid_answer = ['yes', 'y', 'no', 'n']
        while correct not in valid_answer:
            correct = input('Is this correct? \n')
        if correct in ['yes', 'y']:
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
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['Month'] = df['Start Time'].dt.month
    popular_month = df['Month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = months[popular_month-1].title()
    print('The most common month is {}.'.format(popular_month))

    # display the most common day of week
    df['Day of Week'] = df['Start Time'].dt.weekday_name
    popular_day = df['Day of Week'].mode()[0]
    print('The most common day of week is {}.'.format(popular_day))

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    popular_hour = df['Hour'].mode()[0]
    print('The most common start hour is {}.'.format(popular_hour))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most common start station is {}.'.format(popular_start_station))


    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most common end station is {}.'.format(popular_end_station))

    # display most frequent combination of start station and end station trip
    df['Route'] = df['Start Station'] + " to " + df['End Station']
    popular_route = df['Route'].mode()[0]
    print('The most common route is {}.'.format(popular_route))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is {} seconds.'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is {} seconds.'.format(mean_travel_time))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print('Total Subscribers: {}'.format(user_type_count[0]))
    print('Total Customers: {}\n'.format(user_type_count[1]))

    if city == 'washington':
        print('Sorry, no gender or birth year data available for {}.'.format(city.title()))
    else:
        # Display counts of gender
        gender_count = df['Gender'].value_counts()
        print('Total Male Users: {}'.format(gender_count[0]))
        print('Total Female Users: {}\n'.format(gender_count[1]))

        # Display earliest, most recent, and most common year of birth
        birth_yr_oldest = int(df['Birth Year'].min())
        print('The earliest birth year is {}.'.format(birth_yr_oldest))

        birth_yr_youngest = int(df['Birth Year'].max())
        print('The most recent birth year is {}.'.format(birth_yr_youngest))

        birth_yr_common = int(df['Birth Year'].mode()[0])
        print('The most common birth year is {}.'.format(birth_yr_common))


    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        df_raw = df.copy()

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        # give option to print raw data
        see_raw_data = input('\nWould you like to see the raw data?\n')
        index = 0
        if see_raw_data.lower() in ['yes', 'y']:
            while True:
                print(df_raw[index:index+5])
                more = input('\nWould you like to see more?\n')
                if more.lower() not in ['yes', 'y']:
                    break
                else:
                    index += 5

        # give user option to restart and look at more data
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in ['yes', 'y']:
            print('\n\nTHANK YOU FOR EXPLORING US BIKESHARE DATA!\n\n')
            break


if __name__ == "__main__":
	main()
