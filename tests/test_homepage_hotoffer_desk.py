import pytest
from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException

@pytest.fixture
def browser():
  # Initialize ChromeDriver
  driver = Chrome()
  driver.set_window_size(1920, 1024)
  # Wait implicitly for elements to be ready before attempting interactions
  driver.implicitly_wait(5)
  # Return the driver object at the end of setup
  yield driver
  # cleanup, quit the driver
  driver.quit()

def test_homepage_hotoffer_desktop(browser):
  browser.get('https://www.vehiculum.de')

  #locators
  dismiss_cookie_message = browser.find_element_by_xpath('/html/body/div[1]/div/a')
  hot_offers = browser.find_element_by_id('h2-hot-offers')
  hot_offers_first_car = browser.find_element_by_xpath('//*[@id="h2-hot-offers"]/div/div[1]')
  hot_offers_first_car_manufacturer = browser.find_element_by_xpath('//*[@id="h2-hot-offers"]/div/div[1]/div/div[3]/div[1]/h3').get_attribute('innerText')
  hot_offers_first_car_model = browser.find_element_by_xpath('//*[@id="h2-hot-offers"]/div/div[1]/div/div[3]/div[1]/h4').get_attribute('innerText')
  hot_offers_first_car_image = browser.find_element_by_xpath('//*[@id="h2-hot-offers"]/div/div[1]/div/div[2]/img').get_attribute('src')
  #hot_offers_first_car_specs = 
  hot_offers_first_car_price = browser.find_element_by_xpath('//*[@id="h2-hot-offers"]/div/div[1]/div/div[3]/div[2]/span[1]').get_attribute('innerText')
  hot_offer_url_part = "leasing-angebote/"+(hot_offers_first_car_manufacturer+"-"+hot_offers_first_car_model).replace(" ","-").lower()

  #dismiss cookie message
  dismiss_cookie_message.click()

  browser.execute_script("arguments[0].scrollIntoView();", hot_offers)
  hot_offers_first_car.click()

  pdp_url = browser.current_url
  assert hot_offer_url_part in pdp_url
