import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['All','January','February','March','April','May','June']
days = ['All','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
column_names = ['id','Start Time','End Time','Trip Duration (s)','Start Station','End Station','User Type','Gender','Birth Year']

def print_time(start):
    """
    Prints the duration of a particular chunk of code from a given start time to when this function is called.

    Returns nothing.
    """
    print("\nThis took %.5f seconds." %(time.time() - start))       #includes the time for the user to explore the data just to show how long they were in a section (overall section/task duration vs calculation time)


def more_data(df, row_start=5):     #technically the rubric wants this to increment by 5, but I really wanted the months and days of the week to be at 6 and 7 respectively because having orphaned rows for those data was annoying and unnecessary when we know the max number of rows
    """
    Asks the user if they'd like to see a few lines of the data that informed the current stats and prints the data from that request if yes.

    Args:
        (pandas df) df - Current data frame

    Returns nothing.
    """
    print('\n'+'~*'*50+'~\n')
    answer = ''
    row_start = 5       #tracks our iloc row calling portion of the code and gets incremented accordingly
    while not answer in ['Yes','No']:
        answer = input('\tWould you like to see sample data for these statistics? (yes/no) \n\t').title()
        if answer == 'Yes':
            print('\n\tThis table is %d lines long. First %d lines:' % (len(df), min(len(df),5)))       #I wanted the user to have some context on how big of a table they might be scrolling through
            print(df.head())

    if answer == 'Yes':
        answer = ''

    if row_start > len(df):     #if there is no second page, tell them and move on!
        print('\tEnd of the current table. Next stat!\n')
    else:
        while row_start < len(df):
            while not answer in ['Yes','No']:
                try:
                    answer = input('\n\tWould you like to see the next 5 lines? (yes/no) \n\t').title()
                except:
                    print('\tPlease enter yes or no.\n\t')
            if answer == 'Yes':
                print(df.iloc[row_start:row_start+5])
                answer = ''             #reset answer to make the inner while condition true again (*NOT* in...)
                row_start += 5
                if row_start >= len(df):
                    print('\tEnd of the current table. Next stat!\n')
                    break
            else:
                print('\tRoger, next!\n')
                break
    print('\n'+'~*'*50+'~\n')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print(' '+'_'*108+' ')
    print('|'+' '*108+'|')
    print('|  '+' '*30+'Hello! Let\'s explore some US bikeshare data'+' '*31+'  |')
    print('|  '+' '*30+'from Washington, Chicago, and New York City'+' '*31+'  |')
    print('|'+'_'*108+'|')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while not city in CITY_DATA.keys():      #makes sure the input value is one we're expecting from the keys in the CITY_DATA dictionary.
        try:
            city = input('\nWhich city would you like to explore bikeshare data on? \n').lower()
        except:
            print('Please enter a valid city name.')


    # TO DO: get user input for month (all, january, february, ... , june)
    month = ''
    while not month in months:      #makes sure the input value is one we're expecting from the pre-written list at the beginning
        try:
            month = input('\nWould you like to filter the data by month? If yes, enter a month name; if not, type \'all\'\nAvailable months in data: '+', '.join(months[1:])+'\n').title()
        except:
            print('Please enter a valid month filter option.')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while not day in days:      #makes sure the input value is one we're expecting from the pre-written list at the beginning
        try:
            day = input('\nWould you like to filter the data by a particular day of the week? If yes, enter the day of the week; if not, type \'all\'\n').title()
        except:
            print('Please enter a valid day of the week filter option.')
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
    columns = column_names[:len(df.columns)]
    df = pd.read_csv(CITY_DATA[city], header=0, names=columns)
    #print(df.head())
    df['month'] = pd.DatetimeIndex(df['Start Time']).month
    df['day_of_week'] = pd.DatetimeIndex(df['Start Time']).weekday_name
    df['Trip Duration (s)'] = pd.to_numeric(df['Trip Duration (s)'], downcast='float')
    #print(df.head())

    if month != 'All':
        # use the index of the months list to get the corresponding int
        month = months.index(month)
        df = df[df.month==month]
        #print(df.head())

    if day != 'All':
        df = df[df.day_of_week == day]
        #print(df.head())

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])         #made these calculations happen here instead of load_data where we add month and day because they're only relevant here vs the earlier filtering functionality
    df['hour'] = pd.DatetimeIndex(df['Start Time']).hour

    # TO DO: display the most common month
    months_count = df.rename(columns={'id':'Trips'}).groupby(['month']).count()       #renames columns so they're easier to read when printed and stores the count of the grouped variables in a new data frame group
    most_common_month = months[months_count.index[months_count.Trips == months_count.Trips.max()].tolist()[0]]      #return the index (month number) whose value matches the maximum value in the count column (any column that doesn't have any empty values)
    print('The most common month of travel is: \t\t{}'.format(most_common_month))
    more_data(months_count[['Trips']],6)

    # TO DO: display the most common day of week
    days_count = df.rename(columns={'id':'Trips','day_of_week':'Week Day'}).groupby(['Week Day']).count()       #renames columns so they're easier to read when printed and stores the count of the grouped variables in a new data frame group
    most_common_day = days_count[days_count.Trips == days_count.Trips.max()].index.tolist()[0]      #return the index (week day) whose value matches the maximum value in the count column (any column that doesn't have any empty values)
    print('The most common week day to travel is: \t\t{}'.format(most_common_day))
    more_data(days_count[['Trips']],7)

    # TO DO: display the most common start hour
    hours_count = df.rename(columns={'id':'Trips'}).groupby(['hour']).count()       #renames columns so they're easier to read when printed and stores the count of the grouped variables in a new data frame group
    most_common_hour = hours_count[hours_count.Trips == hours_count.Trips.max()].index.tolist()[0]      #return the index (hour number) whose value matches the maximum value in the count column (any column that doesn't have any empty values)
    print('The most common hour of the day to travel is: \t{}'.format(most_common_hour))
    more_data(hours_count[['Trips']])

    print_time(start_time)
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    df['trip'] = df[['Start Station', 'End Station']].agg(' to '.join, axis=1)         #joins the two station columns to create a trip column; this calculation takes a while so I moved it from the load data function to this station_stats function since the column is only used here

    # TO DO: display most commonly used start station
    start_stat_count = df.rename(columns={'id':'Trips'}).groupby(['Start Station']).count()       #renames columns so they're easier to read when printed and stores the count of the grouped variables in a new data frame group
    most_common_start = start_stat_count[start_stat_count.Trips == start_stat_count.Trips.max()].index.tolist()[0]      #return the index (station) whose value matches the maximum value in the count column (any column that doesn't have any empty values)
    print('The most common station to travel from is: \t{}'.format(most_common_start))
    more_data(start_stat_count[['Trips']])

    # TO DO: display most commonly used end station
    end_stat_count = df.rename(columns={'id':'Trips'}).groupby(['End Station']).count()       #renames columns so they're easier to read when printed and stores the count of the grouped variables in a new data frame group
    most_common_end = end_stat_count[end_stat_count.Trips == end_stat_count.Trips.max()].index.tolist()[0]      #return the index (station) whose value matches the maximum value in the count column (any column that doesn't have any empty values)
    print('The most common station to travel to is: \t{}'.format(most_common_end))
    more_data(end_stat_count[['Trips']])

    # TO DO: display most frequent combination of start station and end station trip
    trip_count = df.rename(columns={'id':'Trips'}).groupby(['trip']).count()       #renames columns so they're easier to read when printed and stores the count of the grouped variables in a new data frame group
    most_common_trip = trip_count[trip_count.Trips == trip_count.Trips.max()].index.tolist()[0]      #return the index (trip) whose value matches the maximum value in the count column (any column that doesn't have any empty values)
    print('The most common trip is: \t\t\t{}'.format(most_common_trip))
    more_data(trip_count[['Trips']])

    print_time(start_time)
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration Information...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df["Trip Duration (s)"].sum()/60/60     #trip duration column is in seconds so we divide by 60 twice to get to hours; this sum gets pretty big so we didn't want to just leave it in minutes
    print('Total time customers rented bikes: \t%8.1f hours ' % total_travel_time)

    # TO DO: display mean travel time
    avg_travel_time = df["Trip Duration (s)"].mean()/60     #trip duration column is in seconds so we convert to minutes to be in more understandable units of bike riding time
    print('Average rental time: \t\t%8.1f minutes ' % avg_travel_time)
    more_data(df.rename(columns={'id':'Trip'})[['Trip','Start Time','Trip Duration (s)']].groupby(['Trip']).mean())     #pulling data back out of main data frame because this calculation doesn't create any sub-tables.

    print_time(start_time)
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df.rename(columns={'id':'Users','User Type':'User Type:'})[['User Type:','Users']].groupby(['User Type:']).count()       #renames columns so they're easier to read when printed and stores the count of the grouped variables in a new data frame group
    print('Number of trips by user type: \n')
    print(user_types)
    more_data(df.rename(columns={'id':'Trip'})[['Trip','User Type']])

    # TO DO: Display counts of gender
    if ('Gender' in df.columns):                                                                                    #only calculates stat if the column exists (not washington)
        customer_genders = df.rename(columns={'id':'Users','Gender':'Gender:'})[['Gender:','Users']].groupby(['Gender:']).count()       #renames columns so they're easier to read when printed and stores the count of the grouped variables in a new data frame group
        print('Number of Users by Gender: \n')
        print(customer_genders)
        more_data(df.rename(columns={'id':'Trip'})[['Trip','Gender']])

    # TO DO: Display earliest, most recent, and most common year of birth
    if ('Birth Year' in df.columns):                                                                                #only calculates stat if the column exists (not washington)
        birth_years = df.rename(columns={'id':'Trips'})[['Birth Year','Trips']].groupby(['Birth Year']).count()       #renames columns so they're easier to read when printed and stores the count of the grouped variables in a new data frame group
        most_common_year = birth_years[birth_years.Trips == birth_years.Trips.max()].index.tolist()[0]
        earliest_year = df[['Birth Year']].min()
        latest_year = df[['Birth Year']].max()
        print('Most common customer birth year: \t%4d' % most_common_year)
        print('Earliest customer birth year: \t%4d' % earliest_year)
        print('Latest customer birth year: \t\t%4d' % latest_year)
        more_data(birth_years)      #only had the background data request here because all three values come from the same exact sub-table

    print_time(start_time)
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        filter_time = time.time()
        print("\nApplying filters...")
        df = load_data(city, month, day)
        print("\nData load took %.4f seconds.\n" % (time.time() - filter_time))
        print('-'*40)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break



if __name__ == "__main__":
	main()
