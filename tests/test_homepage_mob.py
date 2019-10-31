import pytest
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

@pytest.fixture
def browser():
  # Initialize ChromeDriver
  opts = Options()
  opts.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1")
  driver = Chrome(options=opts)
  driver.set_window_size(375, 812)
  # Wait implicitly for elements to be ready before attempting interactions
  driver.implicitly_wait(10)
  # Return the driver object at the end of setup
  yield driver
  # cleanup, quit the driver
  driver.quit()


def test_homepage_search_mobile(browser):
  browser.get('https://www.vehiculum.de')

  select_manufacturer_button = browser.find_element_by_id('select-manufacturer')
  select_body_type_button = browser.find_element_by_id('select-body-type')
  audi = browser.find_element_by_id('Audi')
  bmw = browser.find_element_by_id('BMW')
  body_type_small = browser.find_element_by_id('body_type_small')
  body_type_cabrio = browser.find_element_by_id('body_type_cabrio')
  select_budget = browser.find_element_by_id('select-budget')
  finance_rate_to_input = browser.find_element_by_id('finance_rate_to')
  submit_button = browser.find_element_by_id('homepage-find-car')
  save_button_manufacturer = browser.find_element_by_xpath('/html/body/header/div/div[1]/div[1]/div/form/div[4]/div/div/div[3]/button')
  save_button_body_type = browser.find_element_by_xpath('/html/body/header/div/div[1]/div[1]/div/form/div[5]/div/div/div[3]/button')
  save_button_price = browser.find_element_by_xpath('/html/body/header/div/div[1]/div[1]/div/form/div[6]/div/div/div[3]/button')
  dismiss_cookie_message = browser.find_element_by_xpath('/html/body/div[1]/div/a')
 
  #dismiss cookie message
  dismiss_cookie_message.click()
  time.sleep(1)

  #select/enter search values
  select_manufacturer_button.click()
  audi.click()
  bmw.click()
  save_button_manufacturer.click()
  select_body_type_button.click()
  body_type_small.click()
  body_type_cabrio.click()
  save_button_body_type.click()
  select_budget.click()
  finance_rate_to_input.send_keys(400)
  save_button_price.click()

  #assert everything was successfully selected/entered and is displayed correctly
  selected_manufacturer = browser.find_element_by_xpath('//*[@id="select-manufacturer"]/span').get_attribute('innerHTML')
  selected_body_type = browser.find_element_by_xpath('//*[@id="select-body-type"]/span').get_attribute('innerHTML')
  selected_budget = browser.find_element_by_xpath('//*[@id="select-budget"]/span').get_attribute('innerHTML')
  assert selected_manufacturer == 'Audi, BMW'
  assert selected_body_type == "Kleinwagen, Cabrio"
  assert selected_budget == "€400"

  #click submit button
  submit_button.click()
  
  #assert you are on the overview page and found some results
  overview_url = browser.current_url
  list_of_vc_cards = browser.find_elements_by_class_name('vc-card')
  assert "leasing-angebote" in overview_url
  assert len(list_of_vc_cards) > 0


def test_homepage_hotoffer_mobile(browser):
  browser.get('https://www.vehiculum.de')
 
  dismiss_cookie_message = browser.find_element_by_xpath('/html/body/div[1]/div/a')
  hot_offers = browser.find_element_by_id('h2-hot-offers')
  hot_offers_car = browser.find_element_by_xpath('//*[@id="h2-hot-offers"]/div/div/div')

  #dismiss cookie message
  dismiss_cookie_message.click()
  time.sleep(1)
  
  #Scroll into view
  browser.execute_script("arguments[0].scrollIntoView();", hot_offers)
  #Swipe 2 times
  ActionChains(browser).drag_and_drop_by_offset(hot_offers_car, -200, 0).drag_and_drop_by_offset(hot_offers_car, -200, 0).perform()
  #locators for current shown car
  hot_offers_car_manufacturer = browser.find_element_by_xpath('//*[@id="h2-hot-offers"]/div/div/div/div[contains(@aria-hidden,"false")]/div/div[3]/div[1]/h3').get_attribute('innerText')
  hot_offers_car_model = browser.find_element_by_xpath('//*[@id="h2-hot-offers"]/div/div/div/div[contains(@aria-hidden,"false")]/div/div[3]/div[1]/h4').get_attribute('innerText')
  #expected part of url of current shown car
  hot_offer_url_part = "leasing-angebote/"+(hot_offers_car_manufacturer+"-"+hot_offers_car_model).replace(" ","-").lower()
  #click current shown car
  time.sleep(0.5)
  hot_offers_car.click()
  #assert you are on the pdp of clicked car
  pdp_url = browser.current_url
  assert hot_offer_url_part in pdp_url


def test_homepage_brands_mobile(browser):
  browser.get('https://www.vehiculum.de')

  car_brands = browser.find_element_by_xpath('/html/body/main/div/div[2]/div[2]/div')
  dismiss_cookie_message = browser.find_element_by_xpath('/html/body/div[1]/div/a')
  next_brands_button = browser.find_element_by_xpath('/html/body/main/div/div[2]/div[2]/div/div/div/button[2]')

  #dismiss cookie message
  dismiss_cookie_message.click()
  time.sleep(1)

  browser.execute_script("arguments[0].scrollIntoView();", car_brands)
  ActionChains(browser).drag_and_drop_by_offset(car_brands, -200, 0).drag_and_drop_by_offset(car_brands, -200, 0).perform()
  current_brands_list = browser.find_element_by_xpath('/html/body/main/div/div[2]/div[2]/div/div/div/div/div/div[contains(@aria-hidden,"false")]')
  first_brand_in_current_list = browser.find_element_by_xpath('/html/body/main/div/div[2]/div[2]/div/div/div/div/div/div[contains(@aria-hidden,"false")]/a[1]')
  first_brand_href_in_current_list = browser.find_element_by_xpath('/html/body/main/div/div[2]/div[2]/div/div/div/div/div/div[contains(@aria-hidden,"false")]/a[1]').get_attribute('href')
  first_brand_in_current_list.click()

  brand_url = browser.current_url
  assert first_brand_href_in_current_list == brand_url


def test_homepage_other_brands_mobile(browser):
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
