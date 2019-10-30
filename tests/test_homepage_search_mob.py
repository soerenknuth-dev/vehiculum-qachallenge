import pytest
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

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