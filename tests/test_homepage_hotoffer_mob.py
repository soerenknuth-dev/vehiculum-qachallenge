import pytest
import time
from selenium.webdriver import Chrome
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


def test_homepage_hotoffer_mobile(browser):
  browser.get('https://www.vehiculum.de')
 
  dismiss_cookie_message = browser.find_element_by_xpath('/html/body/div[1]/div/a')
  hot_offers = browser.find_element_by_id('h2-hot-offers')
  hot_offers_car = browser.find_element_by_xpath('//*[@id="h2-hot-offers"]/div/div/div')
  hot_offers_car_manufacturer = browser.find_element_by_xpath('//*[@id="h2-hot-offers"]/div/div/div/div[3]/div/div[3]/div[1]/h3').get_attribute('innerText')
  hot_offers_car_model = browser.find_element_by_xpath('//*[@id="h2-hot-offers"]/div/div/div/div[3]/div/div[3]/div[1]/h4').get_attribute('innerText')
  hot_offer_url_part = "leasing-angebote/"+(hot_offers_car_manufacturer+"-"+hot_offers_car_model).replace(" ","-").lower()

  #dismiss cookie message
  dismiss_cookie_message.click()
  time.sleep(1)

  browser.execute_script("arguments[0].scrollIntoView();", hot_offers)
  ActionChains(browser).drag_and_drop_by_offset(hot_offers_car, -200, 0).drag_and_drop_by_offset(hot_offers_car, -200, 0).drag_and_drop_by_offset(hot_offers_car, -200, 0).perform()
  hot_offers_car.click()

  pdp_url = browser.current_url
  assert hot_offer_url_part in pdp_url