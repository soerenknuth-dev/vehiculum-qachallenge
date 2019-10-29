import pytest
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