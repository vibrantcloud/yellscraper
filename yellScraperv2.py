import pandas as pd
from time import time, sleep
from datetime import datetime
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import numpy as np
from collections import defaultdict

class YellScraper():
    """Class for WebScraper
    bunch of functions to manage web scraping
    nice to have : add in rotating proxies speed up gathering.
     """
    page_numbers = []
    pages = []
    df_dict = defaultdict(list)
    pcodes = None

    def __init__ (self,business_name,location):
        self.business_name = business_name
        self.location = location

        self.business_url = None
        
    def post_codes(self,avg_pages=10):

        self.pcodes = pd.read_csv(Path.cwd().joinpath('master_postcodes.txt'),sep=',')
        reg_len = len(self.pcodes.loc[self.pcodes['region'].str.contains(self.location)]['region'].unique())
        
        if  reg_len == 1:
            uk_region = self.pcodes.loc[self.pcodes['region'].str.contains(self.location)]['uk_region'].unique()
            n_pcodes =  self.pcodes.loc[self.pcodes['region'].str.contains(self.location)]['postcode'].nunique()
            
            true_name = self.pcodes.loc[self.pcodes['region'].str.contains(self.location)]['region'].unique()

            poss_time = pd.Timedelta('15seconds') * (n_pcodes * avg_pages)

            print(f"{true_name} is located in the {uk_region} and has {n_pcodes} unique post codes")

            print(f"""If the average nubmer of pages per postcode is {avg_pages} then this will take {poss_time}
note you can change the avg_pages by adding in avg_pages in the method""")
            
            self.pcodes = self.pcodes.loc[self.pcodes['region'].str.contains(self.location)]
        

        elif reg_len == 0:
            print("No partial matches found, please try again")
            sys.exit(1)
        else:
            cities = self.pcodes.loc[self.pcodes['region'].str.contains(self.location)]['region'].unique().tolist()
            print("City not found, did you mean one of these cities?: ")
            for city in cities:
                print(city)
            sys.exit(1)
        


    



    def headers(self):
        return {'User-Agent': """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"""}
    # use this function to add in proxies later.
    
    
    
    def error_handler(self,component):
        if component is None:
            component = np.nan
        else:
            component = component.text
        return component



    def create_pages(self):
        self.post_codes()
        """Parse urls from post code self.pcodes and pages:
        build up our url and start the looping over locations & pages"""
        
        self.url = 'https://www.yell.com/ucs/UcsSearchAction.do?keywords='
        self.business_url =  f'{self.url}{self.business_name}'
        
        for index, row in self.pcodes.iterrows():
            location = row['postcode']
            url = f"{self.business_url}&location={location}"
            self.pages.append(url)
            return self.pages


    
    def container_parser(self):
        """start building up relevant data and pass into dataframe"""
        self.create_pages()
        
        
        for item in self.pages:
            print(item)

            page = requests.get(item,headers=self.headers())
            
            soup = BeautifulSoup(page.content,'html.parser')
            
            page_number_end = soup.find_all('a', class_='btn btn-grey')[-1].text
            
            self.page_numbers = [n for n in range(0, int(page_number_end))]
            
            print(f"Looping through {self.page_numbers[-1]} Pages for {self.location}")
            
            for num in self.page_numbers:
                
                new_url = f"{item}&pageNum={num}"
                
                page = requests.get(new_url,headers=self.headers())
                
                soup2 = BeautifulSoup(page.content,'html.parser')
                
            
                container = soup2.select('.businessCapsule--mainContent')


                for card in container:
                    company_name     = card.find(class_='businessCapsule--name')
                    business_type    = card.find(class_='businessCapsule--classification')
                    phone_number     = card.select_one('span.business--telephoneNumber')
                    business_pcode   = card.find('span', attrs={"itemprop": "postalCode"})
                    business_address = card.find('span',attrs={"itemprop": "addressLocality"})
 

                    company_name = self.error_handler(company_name)
                    business_type = self.error_handler(business_type)
                    phone_number = self.error_handler(phone_number)
                    business_pcode = self.error_handler(business_pcode)
                    business_address = self.error_handler(business_address)


                             # only non textual value.
                    website = card.find('a',attrs={'rel' : 'nofollow noopener'})
                    if website is None:
                        website = np.nan
                    else:
                        website = website.attrs['href']

                    self.df_dict['company_name'].append(company_name)
                    self.df_dict['business_type'].append(business_type)
                    self.df_dict['phone_number'].append(phone_number)
                    self.df_dict['post_code'].append(business_pcode)
                    self.df_dict['business_address'].append(business_address)
                    self.df_dict['webpage'].append(website)


       





        return self.df_dict

    
scraper = YellScraper('Tatoo','Birmingham')

scraper.post_codes(20)

scraper.container_parser()