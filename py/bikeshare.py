import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
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
    # get user input for city (chicago, new york city, washington). Uses a while loop to handle invalid inputs
    city = input("\nWould you like to see data for Chicago, New York or Washington?").lower()
    while city not in ("chicago", "new york", "washington"):
            print("Oops, you entered a wrong city. Please enter Chicago, New York or Washington or check if you have written the city correctly!")
            city = input("\nTry again: Would you like to see data for Chicago, New York or Washington?").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("\nWhich month? Please enter one month from January to June or all for every month:").lower()
    while month not in ("january", "february", "march", "april", "may", "june", "all"):
        print("Oops, you entered a wrong month. Please check if you have written the month correctly!")
        month = input("\nTry Again: Which month? Please enter one month from January to June:").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("\nWhich day? Please enter one day from Monday to Sunday or all for every day:").lower()
    while day not in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"):
        print("Oops, you entered a wrong day. Please check if you have written the day correctly!")
        day = input("\nTry Again: Which day? Please enter one day from Monday to Sunday:").lower()

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable and
    displays lines of raw data for the user.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Showing 5 lines of raw data
    # get user input
    raw_data = input("\nWould you like to see 5 lines of raw data for {}? Please enter 'yes' or 'no': ".format(city.capitalize())).lower()

    def checkRawDataInput(raw_data):
        """checks, if the input of user is wrong"""
        while raw_data not in ("no", "yes"):
                print("\nOops, something went wrong!")
                raw_data = input("\nTry again. Please enter 'yes' or 'no':").lower()

    checkRawDataInput(raw_data)

    # displays 5 lines of raw data
    row_id_start = 0
    row_id_end = 5
    while raw_data != "no":
        print(df[row_index_start:row_index_end])
        raw_data = input("\nWould you like to see 5 further lines of raw data for {}? Please enter 'yes' or 'no': ".format(city.capitalize())).lower()
        checkRawDataInput(raw_data)
        row_id_start +=5
        row_id_end +=5

    # convert the Start Time column to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # extract month and day of week from Start Time to create new columns
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.dayofweek

    # filter by month if applicable
    if month != "all":
        # use the index of the months list to get the corresponding int
        months = ["january", "february", "march", "april", "may", "june"]
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df["month"] == month]

    # filter by day of week if applicable
    if day != "all":
        # use the index of the days list to get the corresponding int
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        day_of_week = days.index(day)
        # filter by day of week to create the new dataframe
        df = df[df["day_of_week"] == day_of_week]

    return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print("Choosen Filter: \nMonth:", month.capitalize(), "\nDay:", day.capitalize())

    # display the most common month
    # filter by month if applicable
    if month == "all":
        popular_month = calendar.month_name[df["month"].mode()[0]]
        print('\nMost Popular Month:', popular_month)

    # display the most common day of week
    if day == "all":
        popular_day = calendar.day_name[df["day_of_week"].mode()[0]]
        print('\nMost Popular Day:', popular_day)

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print('\nMost Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df, month, day):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    print("Choosen Filter: \nMonth:", month.capitalize(), "\nDay:", day.capitalize())

    #  display most commonly used start station
    popular_startStation = df['Start Station'].value_counts().idxmax()
    print('\nMost Popular Start Station:', popular_startStation)

    # display most commonly used end station
    popular_endStation = df['End Station'].value_counts().idxmax()
    print('\nMost Popular End Station:', popular_startStation)

    # display most frequent combination of start station and end station
    popular_combination = df.groupby(["Start Station", "End Station"]).size().idxmax()
    print('\nMost Popular Combination of Start Station and End Station:', popular_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df, month, day):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    print("Choosen Filter: \nMonth:", month.capitalize(), "\nDay:", day.capitalize())

    # display total travel time converted from seconds to days, hours and minutes
    total_time = df["Trip Duration"].sum()
    m, s = divmod(total_time, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    print("\nTotal Travel Time:\n", int(d), "days,", int(h), "hours,", int(m), "minutes and", round(s,2), "seconds")

    # display mean travel time converted from seconds to minutes
    mean_time = df["Trip Duration"].mean()
    m_average, s_average = divmod(mean_time, 60)
    print("\nAverage Travel Time:\n", int(m_average), "minutes and", round(s_average, 2), "seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, month, day, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    print("Choosen Filter: \nMonth:", month.capitalize(), "\nDay:", day.capitalize())

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("\nUser Types and their occurences:\n",user_types.to_string())

    # filter missing data in washington.csv
    if city == "washington":
        print("\nThere is no 'Gender' and 'Birth Year' data for Washington.")
    else:
        # Display counts of gender
        gender_types = df['Gender'].value_counts()
        print("\nGender Types and their occurences:\n",gender_types.to_string())

        # Display earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        mostCommon_Year = df['Birth Year'].mode()[0]
        print("\nEarliest Year:", int(earliest_year), "\nMost Recent Year:", int(recent_year), "\nMost Common Year:", int(mostCommon_Year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df, month, day)
        trip_duration_stats(df, month, day)
        user_stats(df, month, day, city)

        # restart query or not
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
