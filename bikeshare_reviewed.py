import numpy as np
import pandas as pd
import time
import datetime as dt
import click

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

month_options = ('january', 'february', 'march', 'april', 'may', 'june')

weekday_options = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday')

def user_selection(prompt, available_options=('y', 'n')):
      """Selects a specific user for operation"""

    while True:
        user_selection = input(prompt).lower().strip()
        if user_selection == 'end':
            raise SystemExit
        elif ',' not in user_selection:
            if user_selection in available_options:
                break
        elif ',' in user_selection:
            user_selection = [i.strip().lower() for i in user_selection.split(',')]
            if list(filter(lambda x: x in available_options, user_selection)) == user_selection:
                break
        prompt = ("\nPlease provide a valid entry:\n>")
    return user_selection


def get_filters():

    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        city = user_selection("\n Kindly select a preferred city or cities,"
                      " (New York City, Chicago or Washington). Separate"
                      " multiple choices with comma: ", CITY_DATA.keys())
        month = user_selection("\nKindly select preferred month or months from January to June "
                       "Separate multiple months selection with commas: ",
                       month_options)
        day = user_selection("\nKindly select preferred day(s) of the week."
                     " Separate multiple days selection with commas: ", weekday_options)

        start_loading = user_selection("\nGreat, everything is ready now"
                              " Do you want to start loading? (y/n): "
                              .format(city, month, day))
        if start_loading == 'y':
            break
        else:
            print("Okay, please redo selection")
    print('-'*40)
    return city, month, day


def load_data(city, month, day):

    # This part will filter out data according to user selection
    if isinstance(city, list):
        df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city), sort=True)
        try:
            df = df.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time', 'Trip Duration', 'Start Station',
                                     'End Station', 'User Type', 'Gender', 'Birth Year'])
        except:
            pass
    else:
        df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour

    if isinstance(month, list):
        df = pd.concat(map(lambda month: df[df['Month'] ==  (month_options.index(month)+1)], month))
    else:
        df = df[df['Month'] == (month_options.index(month)+1)]

    if isinstance(day, list):
        df = pd.concat(map(lambda day: df[df['Weekday'] ==  (day.title())], day))
    else:
        df = df[df['Weekday'] == day.title()]

    print('-'*40)
    return df

def time_stats(df):
    """Display statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    the_most_common_month = df['Month'].mode()[0]
    print(str(month_options [the_most_common_month-1]).title() + ' is the most common month.')

    # display the most common day of week
    the_most_common_day = df['Weekday'].mode()[0]
    print(str(the_most_common_day) + ' is the most common day of the week.')

    # display the most common start hour
    the_most_common_hour = df['Start Hour'].mode()[0]
    print(str(the_most_common_hour) + ' is the most common start hour.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Display statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    the_most_common_start_station = str(df['Start Station'].mode()[0])
    print(the_most_common_start_station + ' is the most commonly used start station.')

    # display most commonly used end station
    the_most_common_end_station = str(df['End Station'].mode()[0])
    print(the_most_common_end_station + ' is the most commonly used end station.')

    # display most frequent combination of start station and end station trip
    df['Start-End Combination'] = (df['Start Station'] + ' - ' +  df['End Station'])
    the_most_frequent_start_end_combination = str(df['Start-End Combination'].mode()[0])
    print(the_most_frequent_start_end_combination +
          ' is the most frequent combination of start station and end station trip.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Display statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time_traveled = df['Trip Duration'].sum()
    total_time_traveled = (str(int(total_time_traveled//86400)) + 'day(s) ' +
                         str(int((total_time_traveled % 86400)//3600)) + 'hour(s) ' +
                         str(int(((total_time_traveled % 86400) % 3600)//60)) +   'minute(s) and ' +
                         str(int(((total_time_traveled % 86400) % 3600) % 60)) +  'seconds')
    print(total_time_traveled + ', is the total travel time.')

    # display mean travel time
    mean_time_to_travel = df['Trip Duration'].mean()
    mean_time_to_travel = (str(int(mean_time_to_travel//60)) + 'm ' +
                        str(int(mean_time_to_travel % 60)) + 's')
    print(mean_time_to_travel + ", is the mean travel time.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Display statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts for user types: ')
    print(df['User Type'].value_counts().to_string())

    # Display counts of gender
    try: 
        print('\nCounts of gender: ')
        print(df['Gender'].value_counts().to_string())
    except KeyError:
        print('There is no such data available due to your selection')

    # Display earliest, most recent, and most common year of birth
    try: 
        print('\nThe earliest year of birth is: '+ str(int(df['Birth Year'].min())))
        print('The most recent year of birth is: ' + str(int(df['Birth Year'].max()))) 
        print('The most common year of birth is: ' + str(int(df['Birth Year'].mode()[0])))
    except:
        print('There is no such data available due to your selection')

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df, pointer_spot):

    print('\nDisplaying raw data, 5 lines per request>>>')

    if pointer_spot > 0:
        pointer_last_spot = user_selection('\nDo you wish to continue viewing more? (y/n): ')
        if pointer_last_spot == 'n':
            pointer_spot = 0
            pass

    while True:
        for i in range(pointer_spot, len(df.index)):
            print('\n'+ df.iloc[pointer_spot:pointer_spot+5].to_string())
            pointer_spot += 5
            if user_selection('\nDo you wish to continue viewing more raw data? (y/n): ') == 'y':
                continue
            else:
                break
        break
    return pointer_spot




def main():
    while True:
        click.clear()
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        pointer_spot = 0
        while True:
            raw_data_choice = user_selection("\nWould you like to view lines of the Raw Data?: (y/n) ",
                                 ('y', 'n'))
            click.clear()
            if raw_data_choice == 'y':
                pointer_spot = show_raw_data(df, pointer_spot)
                break
            elif raw_data_choice == 'n':
                break


        restart = user_selection("\nOkay now, would you like to restart? (y/n): \n")
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
    main()
