from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd 
from webdriver_manager.chrome import ChromeDriverManager # type: ignore
import uuid 


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
    def __init__(self, url : str = 'https://www.linkedin.com'):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(url)
        self.driver.maximize_window
        time.sleep(2)

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
        except TimeoutException:
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
        my_username = input()
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
    

    def job_search(self,xpath: str = '//*[@id="global-nav-typeahead"]/input') -> None:
        ''' 
        looks for the search bar given in the xpath 
        
        Parameters
        ----------
        xpath:str 
            The xpath of the search bar
        Input():str,optional 
               Contains the job in question

            
            '''

        try:
            time.sleep(0.5)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located)
            engine = self.driver.find_element(By.XPATH , xpath)
            job_text = input()
            engine.send_keys(job_text) 
            engine.send_keys(Keys.RETURN)
            
        except:
            print('pass')

    def enter_jobs(self,xpath: str = '//*[@id="search-reusables__filters-bar"]/ul/li[1]/button') -> None:
        ''' 
        looks for the jobs button given in the xpath 
        
        Parameters
        ----------
        xpath:str 
            The xpath of the search bar

            '''
        time.sleep(2)
        try:
            WebDriverWait(self.driver,20).until(EC.presence_of_element_located)
            enter = self.driver.find_element(By.XPATH,xpath)
            enter.send_keys(Keys.RETURN)
        except:
            print('No enter button')
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

        try:
            lp = bot.driver.find_elements(By.XPATH,'/html/body/div[7]/div[3]/div[3]/div[2]/div/section[1]/div/div/section/div/ul/li')[-1] #finds the final page number and turns data type into an int
            nn = int(lp.find_element(By.XPATH,'./button/span').text)
            if nn <= 10:
                n = nn 
            elif nn > 10:
                n = nn +2
        except NoSuchElementException:
            lp = bot.driver.find_elements(By.XPATH,'/html/body/div[6]/div[3]/div[3]/div[2]/div/section[1]/div/div/section/div/ul/li')[-1] #finds the final page number and turns data type into an int
            nn = int(lp.find_element(By.XPATH,'./button/span').text)
            if nn < 10:
                n = nn 
            elif nn > 10:
                n = nn +2
        for i in range(n):
            time.sleep(0.5)
            try:
                number_container = bot.driver.find_element(By.XPATH,'/html/body/div[6]/div[3]/div[3]/div[2]/div/section[1]/div/div/section/div/ul') # Finds the container for the page numbers
                pages = number_container.find_elements(By.XPATH, './li') #Finds each element in the container 
            except NoSuchElementException:
                number_container = bot.driver.find_element(By.XPATH,'/html/body/div[7]/div[3]/div[3]/div[2]/div/section[1]/div/div/section/div/ul')
                pages = number_container.find_elements(By.XPATH, './li')
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
                for i in range(25):
                    time.sleep(1)
                    try:
                        container = bot.driver.find_element(By.XPATH,'/html/body/div[7]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul') # Finds the container for the jobs 
                        job_list = container.find_elements(By.XPATH,'./li/div/div/div[1]/div[2]/div[1]/a') # Finds each element in the container 
                    except NoSuchElementException:
                        container = bot.driver.find_element(By.XPATH,'/html/body/div[6]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul')
                        job_list = container.find_elements(By.XPATH,'./li/div/div/div[1]/div[2]/div[1]/a')
                    job_list[i].click()
                    try:
                        time.sleep(0.2)
                        links = job_list[i].get_attribute('href')
                        job_dict['Link'].append(links)     
                    except NoSuchElementException:
                        job_dict['Link'].append('No Link found')
                    try:
                        time.sleep(0.2)
                        title = bot.driver.find_element(By.XPATH, '/html/body/div[7]/div[3]/div[3]/div[2]/div/section[2]/div/div/div[1]/div/div[1]/div/div[2]/a/h2')
                        job_dict['Title'].append(title.text)
                    except NoSuchElementException:
                        title = bot.driver.find_element(By.TAG_NAME, 'h1')
                        job_dict['Title'].append(title.text)
                    try:
                        time.sleep(0.2)
                        location = bot.driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[3]/div[2]/div/section[2]/div/div/div[1]/div/div[1]/div/div[2]/div[1]/span[1]/span[2]')
                        job_dict['Location'].append(location.text)
                    except NoSuchElementException:
                        location = bot.driver.find_element(By.XPATH, '/html/body/div[7]/div[3]/div[3]/div[2]/div/section[2]/div/div/div[1]/div/div[1]/div/div[2]/div[1]/span[1]/span[2]')
                        job_dict['Location'].append(location.text)
                    job_dict['UUID'].append(uuid.uuid4)
            except IndexError:
                pass
        pd.DataFrame(job_dict)
                    



if __name__ == '__main__':
    bot = Scraper()
    bot.accept_cookies()
    bot.user_name()
    bot.pass_word()
    bot.job_search()
    bot.enter_jobs()
    bot.info_scrape()

