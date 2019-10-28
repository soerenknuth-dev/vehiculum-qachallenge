import pytest
from selenium.webdriver import Chrome

@pytest.fixture
def browser():
  # Initialize ChromeDriver
  driver = Chrome()
  driver.set_window_size(1920, 1024)
  # Wait implicitly for elements to be ready before attempting interactions
  driver.implicitly_wait(10)
  # Return the driver object at the end of setup
  yield driver
  # cleanup, quit the driver
  driver.quit()


def test_homepage_search(browser):
  # Setup Testcase Data
  URL = 'https://www.vehiculum.de'

  # Navigate to vehiculum Homepage
  browser.get(URL)
  #find and click the manufacturer button
  select_manufacturer_button = browser.find_element_by_id('select-manufacturer')
  select_manufacturer_button.click()
  #find and click "Audi" manufacturer
  audi = browser.find_element_by_id('Audi')
  audi.click()
  #assert Audi was successfully selected
  selected_manufacturer = browser.find_element_by_xpath('//*[@id="select-manufacturer"]/span').get_attribute('innerHTML')
  assert selected_manufacturer == 'Audi'


  