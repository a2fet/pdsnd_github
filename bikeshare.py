import time
import pandas as pd
import numpy as np
## make sure that the .csv files are downloaded from the cloud.
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
    print("\nHello! Let\'s explore some US bikeshare data!")
    # TO DO: get user input for city (chicago, new york city, washington). Use a while loop to handle invalid inputs
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington?\n").lower()
        if city in ('chicago', 'new york city', 'washington'):
            break
        else:
            print("\nYou must enter one of the three cities in the prompt as it is written.")

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nFor which month (January through June) would you like to see data? If you want to see combined data for all six months, type \"all\" .\n").lower()
        if month in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
            break
        else:
            print("\nPlease choose a month in the first half of the year. Enter without abbreviations. If you want to see data for all months January through June, type \"all\".")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nWhich day of the week would you like to explore? If you want to see data for all seven days, type \"all\" .\n").lower()
        if day in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            break
        else:
            print("\nEnter the day without abbreviations, ie \"Friday\". If you want to see data for every day of the week combined, type \"all\".")

    print("\n We'll be exploring data from {} in month: {} and on day: {}".format(city.title(), month.title(), day.title()))
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int (remember input is str, in df it is int)
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_num = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month_num]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe, use .title() because dt.weekday_name returns day capitalized
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    com_month_num = df['month'].mode()
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    com_month = months[int(com_month_num - 1)].title()
    print("The most common month for rides: ", com_month)

    # display the most common day of week
    com_day = df['day_of_week'].mode()[0]
    print("The most common day for rides: ", com_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    com_hour = df['hour'].mode()[0]
    print("The most common starting hour for rides: ", com_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start = df['Start Station'].mode()[0]
    print("Most common station to start a trip: ", pop_start)

    # display most commonly used end station
    pop_fin = df['End Station'].mode()[0]
    print("Most common station to end a trip: ", pop_fin)

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']
    pop_trip = df['trip'].mode()[0]
    pop_trip_freq = len(df[df['trip'] == pop_trip])
    print("Most commonly taken trip is from {} with {} occurences.\n".format(pop_trip, pop_trip_freq))
    print("Here are the five most common trips taken and their frequencies:")
    print(df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).head(5))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    tot_time = df['Trip Duration'].sum()
    dtup = divmod(tot_time, (24*3600))
    htup = divmod(dtup[1], 3600)
    mtup = divmod(htup[1], 60)
    print("Users spent a total of {} days, {} hours, {} minutes, and {} seconds riding.".format(dtup[0],htup[0],mtup[0],int(mtup[1])))

    # TO DO: display mean travel time
    avg_time = df['Trip Duration'].mean()
    htup = divmod(avg_time, 3600)
    mtup = divmod(htup[1], 60)
    print("Users spent an average of {} hours, {} minutes, and {} seconds on each trip.".format(htup[0],mtup[0],int(mtup[1])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("A table showing the count for each user type.")
    print(df['User Type'].value_counts())

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        print("\nA table showing the count for each user gender.")
        nan_num = df['Gender'].isnull().sum()
        print("{} people did not specify their gender.".format(nan_num))
        print(df['Gender'].value_counts())
    else:
        print("This city does not have gender data.")

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("\nBirth year statistics:")
        print("The most recent birth year on record is {}.".format(int(df['Birth Year'].max())))
        print("The earliest birth year on record is {}.".format(int(df['Birth Year'].min())))
        print("The most common birth year among users is {}.".format(int(df['Birth Year'].mode())))
    else:
        print("This city does not have birth year data.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def restart():
    restart = input('\nWould you like to restart? Enter yes or no.\n')
    if restart.lower() != 'yes':
        print("Okay, bye!")
        quit()
    else:
        main()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        raw = input("Would you like to see the first 10 rows of raw data? Enter yes or no.\n")
        if raw.lower() == 'yes':
            print(df.head(10))
            restart()
        elif raw.lower() == 'no':
            restart()
        else:
            print("Your input must be yes or no.")

if __name__ == "__main__":
	main()
