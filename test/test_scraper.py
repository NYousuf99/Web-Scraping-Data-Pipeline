import unittest
from scraper_package import scraper
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

class TestCase(unittest.TestCase):
    def setUp(self):
        self.bot = scraper.Scraper()

    def test_accept_cookies(self):
        self.bot.driver.find_element(By.XPATH,'//*[@id="artdeco-global-alert-container"]/div/section/div/div[2]/button[2]').click()
        time.sleep(0.5)
        self.bot.driver.maximize_window()
        time.sleep(1)
        self.bot.driver.find_element(By.XPATH,'/html/body/nav/a') # This looks for the linkedin logo in the start up page if this changes we know that the scraper needs updating.
        time.sleep(1)

    def test_user_name(self,xpath:str = '//*[@id="session_key"]'):
        time.sleep(2)
        self.bot.driver.find_element(By.XPATH, xpath)

    def test_pass_word(self, xpath: str = '//*[@id="session_password"]'):
        time.sleep(1)
        self.bot.driver.find_element(By.XPATH, xpath)
    
    def test_login_page(self):
        self.bot.accept_cookies()
        self.bot.user_name()
        self.bot.pass_word()
        time.sleep(2)
        actual_value = self.bot.driver.current_url
        expected_value = 'https://www.linkedin.com/feed/?trk=homepage-basic_signin-form_submit'
        self.assertEqual(actual_value,expected_value)

    def test_enter_jobs(self):
        self.bot.accept_cookies()
        self.bot.user_name()
        self.bot.pass_word()
        time.sleep(3)
        self.bot.job_search()
        time.sleep(5)
        job_button = self.bot.driver.find_element(By.XPATH, '//*[@id="search-reusables__filters-bar"]/ul/li[1]/button').get_attribute('aria-label')
        actual_value = job_button
        expected_value = 'Jobs'
        self.assertTrue(actual_value,expected_value)

    def test_pagination(self):
        self.bot.accept_cookies()
        self.bot.user_name()
        self.bot.pass_word()
        time.sleep(1.5)
        self.bot.job_search()
        time.sleep(1.5)
        self.bot.enter_jobs()
        time.sleep(5)
        try:
            self.bot.driver.find_element(By.XPATH,'/html/body/div[7]/div[3]/div[3]/div[2]/div/section[1]/div/div/section/div/ul')
        except NoSuchElementException:
            self.bot.driver.find_element(By.XPATH,'/html/body/div[6]/div[3]/div[3]/div[2]/div/section[1]/div/div/section/div/ul')

    def tearDown(self):
        time.sleep(2)
        self.bot.driver.close()
        
if __name__ == '__main__':
    unittest.main(verbosity=0)

