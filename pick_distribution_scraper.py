from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.options import Options
import pandas as pd

DATA_FILEPATH = 'data/March_Madness_2024_Silver_Bulletin_03_18_2024.csv'
PICK_DATA_FILEPATH = 'data/yahoo_pick_distributions.csv'
NAME_PAIRS_FILEPATH = 'data/name_pairs.csv'
URL = 'https://tournament.fantasysports.yahoo.com/mens-basketball-bracket/pickdistribution'

class Scraper:
    def __init__(self):
        self.options = Options()
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('log-level=3')
        
        self.name_pairs = pd.read_csv(NAME_PAIRS_FILEPATH)

    def get_data(self):
        # Use Selenium to load the webpage and interact with it
        driver = webdriver.Chrome(options=self.options)
        driver.get(URL)
        time.sleep(0.5)  # Wait for page content to load

        # Initialize list to store the data
        data = pd.DataFrame({'team_name': []})

        # Iterate over each tab
        xpaths = [
            f"//html[@id='atomic']//div[@id='main-0-PickDistribution-Proxy']/div/div//div[@class='Fz(16px) Px(15px) Py(8px)']/button[{i}]/div[@class='Px(6px) Py(8px)']" \
            for i in range(1,7)
        ]
        tabs = [driver.find_element(By.XPATH, path) for path in xpaths]
        for tab in range(0,6):
            tabs[tab].click()  # Click on the tab to load its content
            time.sleep(0.5)  # Wait for the content to load
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract data from the table rows
            current_tab = self.extract_data(soup, tab)
            
            # Merge the data from this tab into the master
            data = current_tab if data.shape == (0,1) else pd.merge(data, current_tab, on='team_name')

        # Close the Selenium driver
        driver.quit()

        # Convert names to match Nate Silver data
        data = self.convert_names(data)
        
        # Add playin_flag and seed
        silver_data = pd.read_csv(DATA_FILEPATH)
        silver_data = silver_data.iloc[:, :silver_data.columns.get_loc('rd1_win')]
        data = pd.merge(silver_data, data, on='team_name')
        data.insert(data.columns.get_loc('rd2_pick'), 'rd1_pick', [0.5 if i else 1 for i in data.playin_flag])

        # Save data to csv
        data.to_csv(PICK_DATA_FILEPATH, index=False)

    def extract_data(self, soup, tab):
        teams = []
        percentages = []

        for row in soup.find_all("tr"):
            columns = row.find_all('td')
            if len(columns) == 4:  # Ensure it's a data row with four columns
                team = columns[1].text.strip()
                percentage = float(columns[2].text.strip()[:-1])
                teams.append(team)
                percentages.append(percentage/100)

        return pd.DataFrame({'team_name': teams, f'rd{tab+2}_pick': percentages})
    
    def convert_names(self, data):
        data = pd.merge(data, self.name_pairs, left_on='team_name', right_on='yahoo')\
                    .drop(columns=['yahoo', 'team_name'], inplace=False)\
                    .rename(columns={'silver': 'team_name'}, inplace=False)
        data.insert(0, 'team_name', data.pop('team_name'))
        return data




scraper = Scraper()
scraper.get_data()