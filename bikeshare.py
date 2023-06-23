import time
from datetime import datetime
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!\n")

    cities = ['chicago', 'new york city', 'washington']
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'none']
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'none']

    city = ""
    month = ""
    day = ""

    while city.lower() not in cities:
        city = input("Please enter the name of the city (Chicago, New York City, Washington):\n")
        if city.lower() not in cities:
            print("Invalid city! Please try again.")

    while month.lower() not in months:
        month = input("Please enter the name of the month (January, February, March, April, May, June, or none):\n")
        if month.lower() not in months:
            print("Invalid month! Please try again.")

    while day.lower() not in days:
        day = input("Please enter the name of the day of the week (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or none):\n")
        if day.lower() not in days:
            print("Invalid day! Please try again.")

    return city.lower(), month.lower(), day.lower()

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
    # Load the data file for the specified city
    df = pd.read_csv(CITY_DATA[city])

    # Convert the 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract the month and day of week from the 'Start Time' column to create new columns
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    # Filter by month if applicable
    if month != 'none':
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'none':
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    if month == 'none':
        popular_month = df['month'].mode()[0]
        month_trips = df[df['month'] == popular_month].shape[0]
        print(f"The most popular month is: {popular_month.capitalize()} (with {month_trips} trips)")
    else:
        print("Statistics for the most popular month aren't shown because data is filtered by month.")

    # Display the most common day of week
    if day == 'none':
        popular_day = df['day_of_week'].mode()[0]
        day_trips = df[df['day_of_week'] == popular_day].shape[0]
        print(f"The most popular day of week: {popular_day.capitalize()} (with {day_trips} trips)")
    else:
        print("Statistics for the most popular day of the week aren't shown because data is filtered by day.")

    # Display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    popular_hour = df['Hour'].mode()[0]
    hour_trips = df[df['Hour'] == popular_hour].shape[0]
    print(f"The most popular start hour: {popular_hour} (with {hour_trips} trips)")

    print("\nThis took %s seconds to calculate." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    start_station_trips = df[df['Start Station'] == popular_start_station].shape[0]
    print(f"The most popular start station: {popular_start_station} (with {start_station_trips} trips)")

    # Display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    end_station_trips = df[df['End Station'] == popular_end_station].shape[0]
    print(f"The most popular end station: {popular_end_station} (with {end_station_trips} trips)")

    # Display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    popular_trip = df['Trip'].mode()[0]
    trip_trips = df[df['Trip'] == popular_trip].shape[0]
    print(f"The most popular trip: {popular_trip} (with {trip_trips} trips)")

    print("\nThis took %s seconds to calculate." % (time.time() - start_time))
    print('-' * 40)

def format_duration(duration, units):
    """Formats the duration and units as a string."""
    return f"{duration:.0f} {units}" if duration.is_integer() else f"{duration:.0f} {units}s"

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculate total travel time in seconds
    total_travel_time = df['Trip Duration'].sum()

    # Calculate mean travel time in seconds
    mean_travel_time = df['Trip Duration'].mean()

    # Convert total travel time to higher units if applicable
    if total_travel_time >= 60:
        total_travel_time, seconds = divmod(total_travel_time, 60)
        if total_travel_time >= 60:
            total_travel_time, minutes = divmod(total_travel_time, 60)
            if total_travel_time >= 24:
                total_travel_time, hours = divmod(total_travel_time, 24)
                if total_travel_time >= 30:
                    total_travel_time, days = divmod(total_travel_time, 30)
                    if total_travel_time >= 12:
                        total_travel_time, months = divmod(total_travel_time, 12)
                        total_units = 'years' if total_travel_time >= 1 else 'months'
                        total_travel_time = format_duration(total_travel_time, total_units)
                    else:
                        total_units = 'months' if total_travel_time >= 1 else 'days'
                        total_travel_time = format_duration(total_travel_time, total_units)
                else:
                    total_units = 'days' if total_travel_time >= 1 else 'hours'
                    total_travel_time = format_duration(total_travel_time, total_units)
            else:
                total_units = 'hours' if total_travel_time >= 1 else 'minutes'
                total_travel_time = format_duration(total_travel_time, total_units)
        else:
            total_units = 'minutes' if total_travel_time >= 1 else 'seconds'
            total_travel_time = format_duration(total_travel_time, total_units)
    else:
        total_units = 'seconds'
        total_travel_time = format_duration(total_travel_time, total_units)

    # Convert mean travel time to higher units if applicable
    if mean_travel_time >= 60:
        mean_travel_time, seconds = divmod(mean_travel_time, 60)
        if mean_travel_time >= 60:
            mean_travel_time, minutes = divmod(mean_travel_time, 60)
            if mean_travel_time >= 24:
                mean_travel_time, hours = divmod(mean_travel_time, 24)
                if mean_travel_time >= 30:
                    mean_travel_time, days = divmod(mean_travel_time, 30)
                    if mean_travel_time >= 12:
                        mean_travel_time, months = divmod(mean_travel_time, 12)
                        mean_units = 'years' if mean_travel_time >= 1 else 'months'
                        mean_travel_time = format_duration(mean_travel_time, mean_units)
                    else:
                        mean_units = 'months' if mean_travel_time >= 1 else 'days'
                        mean_travel_time = format_duration(mean_travel_time, mean_units)
                else:
                    mean_units = 'days' if mean_travel_time >= 1 else 'hours'
                    mean_travel_time = format_duration(mean_travel_time, mean_units)
            else:
                mean_units = 'hours' if mean_travel_time >= 1 else 'minutes'
                mean_travel_time = format_duration(mean_travel_time, mean_units)
        else:
            mean_units = 'minutes' if mean_travel_time >= 1 else 'seconds'
            mean_travel_time = format_duration(mean_travel_time, mean_units)
    else:
        mean_units = 'seconds'
        mean_travel_time = format_duration(mean_travel_time, mean_units)

    print(f"Total travel time: {total_travel_time}")
    print(f"Mean travel time: {mean_travel_time}")

    print("\nThis took %s seconds to calculate." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Share of users by type:")
    print(user_types)

    # Display counts of gender if the column exists
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print("\nShare of users by gender:")
        print(gender_counts)

    # Display earliest, most recent, and most common year of birth if the column exists
    if 'Birth Year' in df:
        earliest_year = int(df['Birth Year'].min())
        print(f"\nEarliest year of birth: {earliest_year}")

        most_recent_year = int(df['Birth Year'].max())
        print(f"Most recent year of birth: {most_recent_year}")

        common_year = int(df['Birth Year'].mode()[0])
        print(f"Most common year of birth: {common_year}")

        # Display age group statistics
    if 'Birth Year' in df:
        # Calculate age from birth year
        current_year = datetime.now().year
        df['Age'] = current_year - df['Birth Year']

        # Define age groups (based on US Census age ranges)
        age_groups = {
            'Under 18': df[df['Age'] < 18].shape[0],
            '18-24': df[(df['Age'] >= 18) & (df['Age'] <= 24)].shape[0],
            '25-34': df[(df['Age'] >= 25) & (df['Age'] <= 34)].shape[0],
            '35-44': df[(df['Age'] >= 35) & (df['Age'] <= 44)].shape[0],
            '45-54': df[(df['Age'] >= 45) & (df['Age'] <= 54)].shape[0],
            '55-64': df[(df['Age'] >= 55) & (df['Age'] <= 64)].shape[0],
            '65 and over': df[df['Age'] >= 65].shape[0]
        }

        print("\nShare of users by Age Groups:")
        for group, count in age_groups.items():
            print(f"{group}: {count}")
    else:
        print("\nBirth Year information is not available for this city.")

    print("\nThis took %s seconds to calculate." % (time.time() - start_time))
    print('-' * 40)

def display_raw_data(df):
    """Displays raw data from the dataframe upon user's request."""
    i = 0
    raw = input("Would you like to see the raw data? Enter 'yes' or 'no': ").lower()

    while True:
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df.iloc[i:i+5])
            i += 5
            raw = input("Would you like to see the next 5 lines of raw data? Enter 'yes' or 'no': ").lower()
        else:
            raw = input("Invalid input. Please enter only 'yes' or 'no': ").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Thank you for consulting the date. Have a great day!')
            break


if __name__ == "__main__":
    main()
