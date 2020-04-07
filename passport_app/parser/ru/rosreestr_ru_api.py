from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

def selenium_rosreestr(cadastral_numb):
    result = {}

    binary = FirefoxBinary('/mnt/d/work/python/my_pass/reis/geckodriver')
    # browser = webdriver.Firefox(firefox_binary=binary)
    driver = webdriver.Firefox()
    driver.get("http://www.python.org")
    assert "Python" in driver.title
    elem = driver.find_element_by_name("q")
    elem.clear()
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    driver.close()

    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # options.add_argument('window-size=1200x900')
    # browser = webdriver.Chrome(
    #     # executable_path='/Users/vadim/django/passport/estp/chromedriver',
    #     # executable_path='/opt/django-apps/passport/estp/chromedriver',
    #     # executable_path='/usr/local/bin/chromedriver',
    #     chrome_options=options)
    # browser.set_window_size(1124, 850)  # фейковый размер экрана иначе будет ошибка

    url = 'https://rosreestr.ru/wps/portal/cc_information_online?KN=%s' % cadastral_numb
    #
    # browser.get(url)
    #
    # try:  # нажимаем на кнопку запроса
    #     request_button = WebDriverWait(browser, 5).until(
    #         EC.presence_of_element_located((By.ID, 'submit-button')))
    #     request_button.click()
    # except TimeoutException:
    #     pass
    #
    # try:  # нажимаем на адресс
    #     request_button = WebDriverWait(browser, 5).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR,
    #                                         'td table tbody tr:nth-child(2) td.td:first-child')))
    #     request_button.click()
    # except TimeoutException:
    #     pass
    #
    # try:  # нажимаем на 'Права и ограничения'
    #     request_button = WebDriverWait(browser, 5).until(
    #         EC.presence_of_element_located((By.ID, 'sw_r_enc')))
    #     request_button.click()
    # except TimeoutException:
    #     pass
    #
    # for i in browser.find_elements_by_css_selector('#r_enc tr td'):
    #     i_text = i.text
    #     if i_text.find('Собственность') != -1:
    #         result['ownership'] = i_text
    #     if i.text.find('Аренда') != -1:
    #         result['rent'] = i_text

    return result
