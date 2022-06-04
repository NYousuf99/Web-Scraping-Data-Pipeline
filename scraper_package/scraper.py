from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver import ChromeOptions 
import pandas as pd 
from webdriver_manager.chrome import ChromeDriverManager # type: ignore
# import json
# import jsonpickle 
# from json import JSONEncoder
from sqlalchemy import create_engine
import yaml
import time


class Scraper:
    '''
    This class is a scraper which is used for scraping and browsing different webites

    Parameters
    ----------
    url: str
        This contains the link
    
    Atrribute
    ---------
    driver:
        This is the webdriver object
    '''
    def __init__(self, url : str = 'https://www.linkedin.com', creds: str = 'rds_cred.yaml'):
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')  
        chrome_options.add_argument("--window-size=1200,767")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
        self.driver.get(url)

        with open(creds, 'r') as f:
            creds = yaml.safe_load(f)

        DATABASE_TYPE = creds['DATABASE_TYPE']
        DBAPI = creds['DBAPI']
        HOST = creds['HOST']
        USER = creds['USER']
        PASSWORD = creds['PASSWORD']
        DATABASE = creds['DATABASE']
        PORT = creds['PORT']
        self.engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
        self.df = pd.read_sql('First_bucket',self.engine)
        self.JobID = list(self.df['UUID'])
        

    def accept_cookies(self,xpath: str = '//*[@id="artdeco-global-alert-container"]/div/section/div/div[2]/button[2]') -> None:
        ''' This method looks for and clicks on the accept cookies button
        
        Parameters 
        ----------
        xpath: str
            This contains the xpath of the accept cookies button'''
        time.sleep(2)
        try:
            WebDriverWait(self.driver,15).until(EC.presence_of_element_located)
            self.driver.find_element(By.XPATH,xpath).click()
        except NoSuchElementException:
            print('No cookies found')

    def user_name(self,xpath:str = '//*[@id="session_key"]') -> None:
        ''' 
        This method finds the username bar and asks the developer to enter their username
        
        Parameters
        ----------
        xpath:str 
        input(): str,optional

        '''
        username = self.driver.find_element(By.XPATH, xpath)
        my_username = input("Enter Username:  ")
        username.send_keys(my_username)



    def pass_word(self,xpath:str = '//*[@id="session_password"]') -> None :
        ''' 
        This method finds the password bar and asks the developer to enter their password
        
        Parameters
        ----------
        xpath:str
            The xpath for the password bar
        getpass(): str,optional
            Ask the developer to enter their password
        
        '''
        password = self.driver.find_element(By.XPATH,xpath)
        my_password = getpass()
        password.send_keys(my_password)
        password.send_keys(Keys.RETURN)
    

    def job_search(self,xpath: str = '/html/body/div[7]/header/div/div/div/div[1]/input') -> None:
        ''' 
        looks for the search bar given in the xpath 
        
        Parameters
        ----------
        xpath:str 
            The xpath of the search bar
        Input():str,optional 
               Contains the job in question

            
            '''
    
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located)
        engine = self.driver.find_element(By.XPATH , xpath)
        job_text = input("Enter job role:  ")
        engine.send_keys(job_text) 
        time.sleep(2)
        engine.send_keys(Keys.RETURN)
        time.sleep(2)

    def enter_jobs(self,xpath: str = '//*[@id="search-reusables__filters-bar"]/ul/li[1]/button') -> None:
        ''' 
        looks for the jobs button given in the xpath 
        
        Parameters
        ----------
        xpath:str 
            The xpath of the search bar
          
          '''
        time.sleep(5)
        try:
            WebDriverWait(self.driver,100).until(EC.presence_of_element_located)
            enter = self.driver.find_element(By.XPATH,xpath)
            enter.click()
        except NoSuchElementException:
            self.driver.find_element(By.LINK_TEXT, 'Jobs').click()
        time.sleep(3)
       
    

    def info_scrape(self) -> None:
        '''
        Finds container for page numbers and container for the jobs of each page and scrapes the information and appends to a dictionary

        '''
        job_dict = {
        'UUID':[],
        'Link': [],
        'Title': [],
        'Location': [],} #type:dict

        time.sleep(2)
        lp = self.driver.find_elements(By.XPATH,'/html/body/div[7]/div[3]/div[4]/div/div/main/div/section[1]/div/div[7]/ul/li')[-1] #finds the final page number and turns data type into an int
        nn = int(lp.text)
        if nn <= 10:
            n = nn 
        elif nn > 10:
            n = nn +2
        for i in range(n):
            time.sleep(2)
            try:
                number_container = self.driver.find_element(By.XPATH,'/html/body/div[7]/div[3]/div[4]/div/div/main/div/section[1]/div/div[7]/ul') # Finds the container for the page numbers
                pages = number_container.find_elements(By.TAG_NAME, 'li') #Finds each element in the container 
            except NoSuchElementException:
                number_container = self.driver.find_element(By.XPATH,'/html/body/div[7]/div[3]/div[4]/div/div/main/div/section[1]/div/div[6]/ul') # Finds the container for the page numbers
                pages = number_container.find_elements(By.TAG_NAME, 'li') #Finds each element in the container 
            if i == 0:
                pass
            elif 0< i and i<9:
                time.sleep(0.5)
                pages[i].click()
            elif 9<i and i<range(n)[-8] :
                time.sleep(0.5)
                pages[6].click()
            elif i> range(n)[-8]:
                time.sleep(0.5)
                pages[i-range(n)[-10]].click()
            try:
                for j in range(25):
                    time.sleep(1)
                    container = self.driver.find_element(By.XPATH,'/html/body/div[7]/div[3]/div[4]/div/div/main/div/section[1]/div/ul') # Finds the container for the jobs 
                    job_list = container.find_elements(By.XPATH,'./li') # Finds each element in the container 
                    job_list[j].click()
                    job_id = job_list[j].get_attribute('data-occludable-job-id')
                    if job_id in job_dict['UUID'] or job_id in self.JobID :
                        pass
                    else:
                        job_dict['UUID'].append(job_id)
                        try:
                            time.sleep(0.2)
                            links = job_list[j].find_element(By.TAG_NAME, 'a').get_attribute('href')
                            job_dict['Link'].append(links)     
                        except NoSuchElementException:
                            job_dict['Link'].append('No Link found')
                        try:
                            time.sleep(0.2)
                            tabel = self.driver.find_element(By.XPATH,'/html/body/div[7]/div[3]/div[4]/div/div/main/div/section[2]')
                            title = tabel.find_element(By.TAG_NAME, 'h2').text
                            job_dict['Title'].append(title)
                        except NoSuchElementException:
                            tabel = self.driver.find_element(By.XPATH,'/html/body/div[7]/div[3]/div[4]/div/div/main/div/section[2]')
                            title = tabel.find_element(By.TAG_NAME, 'h1').text
                            job_dict['Title'].append(title)
                        try:
                            time.sleep(0.2)
                            tabel = self.driver.find_element(By.XPATH,'/html/body/div[7]/div[3]/div[4]/div/div/main/div/section[2]')
                            location = tabel.find_elements(By.TAG_NAME, 'span')
                            job_dict['Location'].append(location[4].text)
                        except NoSuchElementException:
                            job_dict['Location'].append('No Location found')
            except IndexError:
                pass
        JobPd= pd.DataFrame.from_dict(job_dict)
        JobPd.to_sql('First_bucket', self.engine, if_exists = 'append')
        
   


        
        
                    



if __name__ == '__main__':
    bot = Scraper()
    bot.accept_cookies()
    bot.user_name()
    bot.pass_word()
    bot.job_search()
    bot.enter_jobs()
    bot.info_scrape()
    # bot.data_upload()
    # bot.data_edit()

#%%
# %%
