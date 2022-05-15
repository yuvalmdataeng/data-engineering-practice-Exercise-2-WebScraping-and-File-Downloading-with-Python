import pandas as pd
import requests
import os
import pandas
import sys
from bs4 import BeautifulSoup as bs

# Build the URL required to download this file, and write the file locally.
# Open the file with Pandas and find the records with the highest HourlyDryBulbTemperature.
# Print this to stdout/command line/terminal.

def main():
    url = 'https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/'
    Last_Modified = '2022-02-07 14:03  '

    resp = requests.get(url)
    soup = bs(resp.text, 'html.parser')
    # print(type(soup))
    # print(soup)
    # Attempt to web scrap/pull down the contents of https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/
    td = soup.find_all('td', {'align': 'right'})
    for i in td:
        c = i.contents[0]
        # Analyze it's structure, determine how to find the corresponding file to 2022-02-07 14:03 using Python.
        if c == Last_Modified:
            print(c)
            csv = i.parent.contents[0].contents[0].attrs['href']
            print(csv)
            csv_link = f'https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/{csv}'
            break
    print(csv_link)

    path = '/Users/yuval.mutseri/repos/data-engineering-practice/Exercises/Exercise-2/csv'
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print(f"The new directory {path} is created!")
    else:
        print(f"The directory {path} already exist")
    r = requests.get(csv_link)
    save_path = '/Users/yuval.mutseri/repos/data-engineering-practice/Exercises/Exercise-2/csv'
    file_name = csv_link.split("/")[-1]
    completeName = os.path.join(save_path, file_name)
    with open(completeName, 'wb') as f:
        f.write(r.content)
    print(completeName, "Was written")
    df = pd.read_csv(completeName)
    max_HourlyDryBulbTemperature = max(df['HourlyDryBulbTemperature'])
    sys.stderr.write("This is the max_HourlyDryBulbTemperature: ")
    sys.stderr.write(str(max_HourlyDryBulbTemperature))
if __name__ == '__main__':
    main()