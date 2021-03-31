import time
import numpy as np
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv', 'new york':'new_york_city.csv', 'washington': 'washington.csv'}

CITIES = ['chicago','new york', 'washington']
MONTHS = ['january', 'february', 'march','april','may','june','all']
DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello!  Welcome to Dan\'s Bikeshare!  Let\'s look at US bikeshare data')

    # requests for user input on city
    city = None
    while city not in CITIES:
        city = input ('1. Please type preferred city (e.g., chicago, new york, washington): ').lower()

    # requests for user input on month
    month = None
    while month not in MONTHS:
        month = input('2. Please type month.  You can type \'all\' to apply no month filter (e.g., all, january, february, march, april, may, june): ').lower()

    # requests for user input on day
    day = None
    while day not in DAYS:
        day = input ('3. Please type weekday.  You can type \'all\' to apply no day filter (e.g., all, sunday, monday, tuesday, wednesday, thursday, friday, saturday): ').lower()

    print('*'*50)
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
    # loads city-specific data file into dataframe
    df = pd.read_csv(CITY_DATA[city])

    # date-formats 'Start Time' and create separate columns for month, day of week, and hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filters by month if applicable and creates new dataframe
    if month !='all':
        month = MONTHS.index(month)+1
        df = df[df['month'] == month]

    # filters by day if applicable and creates new dataframe
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

# Displays most common month, most common day of week, and most common start hour
def time_stats(df):
    print('\nCalculating the most frequent times of travel...\n')
    start_time = time.time()

    # calculates most common month
    most_common_month = df['month'].value_counts().idxmax()
    print("The most common month is: ", most_common_month)

    # calculates most common day of week
    most_common_day_of_week = df['day_of_week'].value_counts().idxmax()
    print("The most common day of week is: ", most_common_day_of_week)

    # calculates most common start hour
    most_common_start_hour = df['hour'].value_counts().idxmax()
    print("The most common start hour is: ", most_common_start_hour)

    # calculates time it took to calculate time stats info
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*50)

# Displays most commonly used start station. end station, and combination of start and end station
def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # calculates most common start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print("Commonly Used Start Station: ", most_common_start_station)

    # calculates most common end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print("Commonly Used End Station: ", most_common_end_station)

    # calculates most common start and end station
    most_frequent_combination = df.groupby(['Start Station','End Station'],as_index=False).count().sort_values(by=['Start Time'], ascending = False).iloc[0]
    print("Commonly Used Start and End Station: {}, {}".format(most_frequent_combination[0], most_frequent_combination[1]))

    # calculates time it took to calculate station stats info
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*50)

# Displays total travel time and average travel time
def trip_duration_stats (df):
    print('\n Calculating Trip Duration...\n')
    start_time = time.time()

    # calculates total travel time via summation of trip duration
    total_travel = df['Trip Duration'].sum()
    print("Total Travel Time: ", total_travel)

    # calculates aveage travel by taking the average of trip duration
    mean_travel = df['Trip Duration'].mean()
    print("Mean Travel Time: ", mean_travel)

    # calculates time it took to calculate trip duration info
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*50)

# Displays counts of user types, counts of gender, and earliest, most recent, and most common year of birth
def user_stats (df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # calculates number of user types
    print('Counts of user types:\n')
    user_counts = df['User Type'].value_counts()
    print(user_counts)
    print()

    print ("Counts of gender:\n")
    # no gender column results in "not available"
    if 'Gender' not in df:
        print('not available')
    # gender column results in calculating count by gender type
    else:
        gender_counts = df['Gender'].value_counts()
        print(gender_counts)
    print()

    # no birth year column results in "not available"
    if 'Birth Year' not in df:
        print('The most common birth year: not available')
    # birth year column results in calculating most frequent birth year
    else:
        most_common_birth_year = df['Birth Year'].value_counts().idxmax()
        print ("The most common birth year: ", most_common_birth_year)

    # no birth year column results in "not available"
    if 'Birth Year' not in df:
        print('The most recent birth year: not available')
    # birth year column results in calculating max of birth year
    else:
        most_recent_birth_year = df['Birth Year'].max()
        print("The most recent birth year: ", most_recent_birth_year)

    # no birth year column results in "not available"
    if 'Birth Year' not in df:
        print('The earliest birth year: not available')
    # birth year column results in calculating min of birth year
    else:
        earliest_birth_year = df['Birth Year'].min()
        print("The earliest birth year: ", earliest_birth_year)

    # calculates time it took to calculate user stats info
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*50)

# Displays rows of raw data in increments of 5 upon user request
def display_rawdata (df):
    # requests for user input for 5 rows of raw data
    show_data = input('\nWould you like to see 5 rows of data? yes or no: ').lower()
    # prints out first 5 rows of data if user said yes
    if show_data == 'yes':
        print(df.head(5))
        i = 10
        #df.shape[0] gives number of rows
        # considers additional rows of raw data upon user request
        while (i<df.shape[0]):
            # requests for user input for additional 5 rows
            show_more_data = input('\n5 more rows of data? yes or no: ').lower()
            # prints out another 5 rows of data, and will continue until user says no
            if show_more_data == 'yes':
                print(df.head(i))
                i+=5
            else:
                break

def main():
    while True:

        city, month, day = get_filters() # Get user input for city, month, day
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_rawdata(df)

        restart = input('\nWould you like to restart?  Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
