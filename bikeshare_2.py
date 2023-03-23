import time
import pandas as pd
import numpy as np
from tabulate import tabulate

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    cities = ["chicago", "new york city", "washington"]
    months = ["all", "january", "february", "march", "april", "may", "june"]
    days = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid
    # inputs

    while True:
        city = input('Would you like to see data for Chigaco, New York City or Washington?\n').lower()
        if city in cities:
            print('Looks like you to hear about {}! if this not true, restart the program now!\n'.format(city))
            break
        else:
            print('Oops! Looks like you entered an invalid city!')

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input(
            'Which month would like to filter the data by? all, january, february, march, april, may or june?\nPlease '
            'enter the full month name.\n').lower()
        print('\n')
        if month in months:
            break
        else:
            print('Oops! Looks like you entered an invalid month!')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Which day would like to filter the data by? all, monday, tuesday, wednesday, thursday, friday, '
                    'saturday or sunday?\nPlease enter the full day name.\n').lower()
        print('\n')
        if day in days:
            break
        else:
            print('Oops! Looks like you entered an invalid day!')

    print('-' * 40)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

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

    # TO DO: display the most common month
    common_month = df['Start Time'].dt.month.value_counts().idxmax()
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('Most Common Month: {}\n'.format(months[common_month - 1].title()))

    # TO DO: display the most common day of week
    common_day = df['Start Time'].dt.day_name().value_counts().idxmax()
    print('Most Common day: {}\n'.format(common_day))

    # TO DO: display the most common start hour
    common_hour = df['Start Time'].dt.hour.value_counts().idxmax()
    print('Most Common hour: {}\n'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].value_counts().idxmax()
    print('Most Common Start Station: {}\n'.format(common_start))

    # display most commonly used end station
    common_end = df['End Station'].value_counts().idxmax()
    print('Most Common End Station: {}\n'.format(common_end))

    # display most frequent combination of start station and end station trip
    common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most Common Trip: From {} To {}\n'.format(common_trip[0], common_trip[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('Total Travel Time: {}\n'.format(pd.Timedelta(seconds=total_time)))

    # display mean travel time
    average_time = df['Trip Duration'].mean()
    print('Average Travel Time: {}\n'.format(pd.Timedelta(seconds=average_time)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    try:
        user_types = df['User Type'].value_counts()
        print("Users Types\n")
        print(user_types)
        print('\n')
    except KeyError:
        print('No type data to share\n')
    finally:
        # TO DO: Display counts of gender
        try:
            gender = df['Gender'].value_counts()
            print("Users Genders\n")
            print(gender)
            print('\n')
        except KeyError:
            print('No gender data to share\n')
        finally:
            # Display earliest, most recent, and most common year of birth
            try:
                oldest = int(df['Birth Year'].min())
                youngest = int(df['Birth Year'].max())
                most_common_year_of_birth = int(df['Birth Year'].value_counts().idxmax())
                print(
                    'Oldest, Youngest and Most Popular Birth Year: {}, {}, {}'.format(oldest, youngest,
                                                                                      most_common_year_of_birth))
            except KeyError:
                print('No birth year data to share\n')
            finally:
                print("\nThis took %s seconds." % (time.time() - start_time))
                print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        i = 0
        while i < len(df):
            display = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
            if display.lower() != 'yes':
                break
            print(tabulate(df.iloc[np.arange(0+i, 5+i)], headers="keys"))
            i += 5

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
