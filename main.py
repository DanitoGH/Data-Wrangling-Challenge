# modules import
import requests
from bs4 import BeautifulSoup
from csv import writer
import pandas as pandasForSortingCSV


'''
 A function to sort generated csv file 
 and overwrite the unsorted version.
'''
def sort_and_overwrite_csv():
    try:
        # CSV file name
        filename = "./data/eu_road_safety_statistics.csv"
        # Read the unsorted csv file
        csvData = pandasForSortingCSV.read_csv(filename) 
        # Sort data frame by "Road deaths per Million Inhabitants" in decending order
        csvData.sort_values(["Road deaths per Million Inhabitants"], axis=0, ascending=False, inplace=True)
        # Save the sorted csv file to overwrite the unsorted version
        csvData.to_csv(filename)
    except Exception as e:
        print("An exception occurred: ", e) 

# Declare target webiste URL
url = "https://en.wikipedia.org/wiki/Road_safety_in_Europe"
# Initialize GET request 
page = requests.get(url)
# Parse requests response data into a valid HTML with Beautiful Soup
soup = BeautifulSoup(page.text, 'html.parser')

# Initilize csv file creation
with open('./data/eu_road_safety_statistics.csv', 'w', newline='', encoding = 'utf8') as output_file_name:
    # Set csv file name to writer
    thewriter = writer(output_file_name)
    # Declare csv file header
    header = ['Country','Area','Population','GDP per capita', 'Population density', 
    'Vehicle ownership', 'Total road deaths', 'Road deaths per Million Inhabitants',' Year']
    thewriter.writerow(header)
    
    # Empty list to hold the all countries statistics data
    countries_data_list=[]
    # Find a table with a matching class name in the scrapped page data
    europe_road_safety_in_table = soup.find('table',  class_ ='wikitable sortable')
    # Loop through table body to access table rows (tr)
    for countries_table in europe_road_safety_in_table.find_all('tbody'):
        tr_rows = countries_table.find_all('tr')
        # Loop through the table rows to access table data (td)
        for tr_row in tr_rows:
            # Declare an empty list to hold each country statistics data
            country_stats_row_list = []
            
            # Find all available table data (td) and loop through all to extract it content
            country_data = tr_row.find_all('td')
            for data_row in country_data:
                # Append country stats data to country_stats_row_list on each iteration
                country_stats_row_list.append(data_row.text.strip())
            # Append each country's stats data list to all countries data list to create a two-dimensional lists
            countries_data_list.append(country_stats_row_list)
        # Loop through to extract country raw data
        for country_data_list in countries_data_list:
            if len(country_data_list) == 11:
                # Extract country's statistics data by index
                country = country_data_list[0]
                area = country_data_list[1]
                population = country_data_list[2]
                GDP_per_capita = country_data_list[3]
                population_density = country_data_list[4]
                vehicle_ownership = country_data_list[5]
                total_road_deaths = country_data_list[7]
                road_deaths_per_million_inhabitants = country_data_list[8]
                year = 2018 # year is hard coded becuase it value will always be 2018 as stated in the challenge
                # Create a list of countries data to append to csv file column content on each iteration
                country_statistics = [country, area, population, GDP_per_capita,population_density,vehicle_ownership,total_road_deaths,road_deaths_per_million_inhabitants,year]
                thewriter.writerow(country_statistics)

# Invoke this function only when a new unsorted csv file is created  
sort_and_overwrite_csv()
