import time
import pandas as pd
import numpy as np

# List cities and perspective csv files
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
# List months of a year              
months=[ 'january' , 'february' , 'march', 'april', 'may', 'june' ,  'july' , 'august' , 'september' , 'october' , 
                    'november' , 'december' ]
day_of_weeks=[ 'monday' , 'tuesday' , 'wednesday' , 'thursday' , 'friday' , 'saturday' , 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=''
    month=''
    day=''
    key_cities=list(CITY_DATA.keys())
    while city not in key_cities:
        city=input("Enter a city name that is one of these options(chicago, new york city, washington : ").strip().lower()       
    # Get user input for month (all, january, february, ... , june)
    while month not in months and month != 'all':
            month=input("Enter a month that is one of these options (all, january..., december): ").strip().lower()

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while (day not in day_of_weeks) and (day != 'all'):
        day=input("Enter a day that is one of these options(all, monday, tuesday,... sunday): ").strip().lower()

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
    
    df=pd.read_csv(CITY_DATA[city])
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['month']=df['Start Time'].dt.month
    df['day_of_week']=df['Start Time'].dt.dayofweek
    if month!='all':           
       month=months.index(month)+1
       df=df[df['month']==month]
    if day!='all':           
       day=day_of_weeks.index(day)
       df=df[df['day_of_week']==day]        
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    if df.empty:
        print("The result search is empty, so that we can't get the outputs ")
        return
    month_counts= df['month'].value_counts()
    print("The most common month: {} , count: {}\n".format(months[month_counts.index[0]-1],month_counts.values[0]))
    # Display the most common day of week
    day_of_week_counts=df['day_of_week'].value_counts()
    print("The most common day of week: {} , count: {}\n".format(day_of_weeks[day_of_week_counts.index[0]],day_of_week_counts.values[0]))
    # Display the most common start hour
    df['hour']=df['Start Time'].dt.hour
    start_hour_counts=df['hour'].value_counts()
    print("The most common start hour : {} , count : {}\n".format(start_hour_counts.index[0],start_hour_counts.values[0]))     
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    if df.empty:
        print("The result search is empty, so that we can't get the outputs\n")
        return
    df['Start-End Station']= df['Start Station'].str.cat(df['End Station'],sep='-->')

    # Display most commonly used start station
    start_station_counts=df['Start Station'].value_counts()
    print("The most commonly used start station : {} , count : {}\n".format(start_station_counts.index[0],start_station_counts.values[0]))

    # Display most commonly used end station
    end_station_counts=df['End Station'].value_counts()
    print("The most commonly used end station : {} , count : {}\n".format(end_station_counts.index[0],end_station_counts.values[0]))

    # Display most frequent combination of start station and end station trip
    start_end_station_counts=df['Start-End Station'].value_counts()
    print("The most commonly combination of start station and end station trip : {} , count : {}\n".format(start_end_station_counts.index[0],start_end_station_counts.values[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    if df.empty:
        print("The result search is empty, so that we can't get the outputs")
        return
    # Display total travel time
    totalTime=df['Trip Duration'].sum()
    print("The total travel time : {}\n".format(totalTime))

    # Display mean travel time
    meanTime=df['Trip Duration'].mean()
    print("The mean travel time : {}\n".format(meanTime))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    if df.empty:
        print("The result search is empty, so that we can't get the outputs")
        return
    # Display counts of user types
    count_user_types = df['User Type'].value_counts()
    print("counts of user types :\n {}\n".format(count_user_types))

    # Display counts of gender
    if 'gender' not in df.columns.str.lower():
        print("There isn't Gender column in the CSV file")
    else:
        count_genders = df['Gender'].value_counts()
        print("counts of genders : {}\n".format(count_genders))

    # Display earliest, most recent, and most common year of birth
    if 'birth year' not in df.columns.str.lower():
        print("There isn't Birth Year column in the CSV file")
    else:
        count_birth_years = df['Birth Year'].value_counts()
        sort_birth_years=count_birth_years.sort_index(level=int)
        print("The most common year of birth : {}, count : {}\n".format(int(count_birth_years.index[0]),count_birth_years.values[0]))
        print("The earliest year of birth : {}, count : {}\n".format(int(sort_birth_years.index[0]),sort_birth_years.values[0]))
        print("The recent year of birth : {}, count : {}\n".format(int(sort_birth_years.index[-1]),sort_birth_years.values[-1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_next_5_rows(df):
    """Displays the next 5 rows of data."""
    print('\nView the raw data.... \n')
    if df.empty:
        print("The result search is empty, so that we can't view the raw data")
        return
    i=0
    while True:        
        view = input('\nWould you like to view next 5 line? Enter yes or no.\n')
        if view.lower() != 'yes':           
            break
        df_next_5_rows=df.iloc[5*i:5*(i+1)].to_dict(orient='records')
        print('The 5 line raw data : \n',df_next_5_rows)
        i+=1
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_next_5_rows(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
