import pytest
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys

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


def test_homepage_search_desktop(browser):
  browser.get('https://www.vehiculum.de')

  select_manufacturer_button = browser.find_element_by_id('select-manufacturer')
  select_body_type_button = browser.find_element_by_id('select-body-type')
  audi = browser.find_element_by_id('Audi')
  bmw = browser.find_element_by_id('BMW')
  body_type_small = browser.find_element_by_id('body_type_small')
  body_type_cabrio = browser.find_element_by_id('body_type_cabrio')
  select_budget = browser.find_element_by_id('select-budget')
  submit_button = browser.find_element_by_id('homepage-find-car')
  dismiss_cookie_message = browser.find_element_by_xpath('/html/body/div[1]/div/a')
  
  #dismiss cookie message
  dismiss_cookie_message.click()

  #select/enter search values
  select_manufacturer_button.click()
  audi.click()
  bmw.click()
  select_body_type_button.click()
  body_type_small.click()
  body_type_cabrio.click()
  select_budget.send_keys(400)

  #assert everything was successfully selected/entered and is displayed correctly
  selected_manufacturer = browser.find_element_by_xpath('//*[@id="select-manufacturer"]/span').get_attribute('innerHTML')
  selected_body_type = browser.find_element_by_xpath('//*[@id="select-body-type"]/span').get_attribute('innerHTML')
  selected_budget = browser.find_element_by_id('select-budget').get_attribute('value')
  assert selected_manufacturer == 'Audi, BMW'
  assert selected_body_type == "Kleinwagen, Cabrio"
  assert selected_budget == "400"

  #click submit button
  submit_button.click()

  #assert you are on the overview page and found some results
  overview_url = browser.current_url
  count = int(browser.find_element_by_class_name('vc-total-count').get_attribute('innerHTML'))
  list_of_vc_cards = browser.find_elements_by_class_name('vc-card')
  assert "leasing-angebote" in overview_url
  assert count > 0
  assert len(list_of_vc_cards) > 0


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

  #Scroll into view
  browser.execute_script("arguments[0].scrollIntoView();", hot_offers)
  #Click first car in hot offers list
  hot_offers_first_car.click()
  #assert you are on the pdp of clicked car
  pdp_url = browser.current_url
  assert hot_offer_url_part in pdp_url


def test_homepage_brands_desktop(browser):
  browser.get('https://www.vehiculum.de')

  car_brands = browser.find_element_by_xpath('/html/body/main/div/div[2]/div[2]/div')
  dismiss_cookie_message = browser.find_element_by_xpath('/html/body/div[1]/div/a')
  
  #dismiss cookie message
  dismiss_cookie_message.click()
  time.sleep(1)

  browser.execute_script("arguments[0].scrollIntoView();", car_brands)
  current_brands_list = browser.find_element_by_xpath('/html/body/main/div/div[2]/div[2]/div/div/div/div/div/div[contains(@aria-hidden,"false")]')
  first_brand_in_current_list = browser.find_element_by_xpath('/html/body/main/div/div[2]/div[2]/div/div/div/div/div/div[contains(@aria-hidden,"false")]/a[1]')
  first_brand_href_in_current_list = browser.find_element_by_xpath('/html/body/main/div/div[2]/div[2]/div/div/div/div/div/div[contains(@aria-hidden,"false")]/a[1]').get_attribute('href')
  first_brand_in_current_list.click()

  pdp_url = browser.current_url
  assert first_brand_href_in_current_list == pdp_url


def test_homepage_other_brands_desktop(browser):
  browser.get('https://www.vehiculum.de')

  car_brands = browser.find_element_by_xpath('/html/body/main/div/div[2]/div[2]/div')
  dismiss_cookie_message = browser.find_element_by_xpath('/html/body/div[1]/div/a')
  other_brands = browser.find_element_by_xpath('//a[@id="other-brands"]/span')
  other_brands_href = browser.find_element_by_id('other-brands').get_attribute('href')

  
  #dismiss cookie message
  dismiss_cookie_message.click()
  time.sleep(1)

  browser.execute_script("arguments[0].scrollIntoView();", car_brands)
  browser.execute_script("window.scrollBy(0, -100);")
  other_brands.click()
  overview_url = browser.current_url
  assert other_brands_href == overview_url