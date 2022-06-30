import os, random, time

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import (
    ElementNotSelectableException,
    NoSuchElementException,
    TimeoutException,
)

# handle alert window to accept
def handle_alert():
    try:
        WebDriverWait(driver, 5).until(
            expected_conditions.alert_is_present(),
            "Timed out waiting for simple alert to appear",
        )
        alert = driver.switch_to.alert
        alert.accept()
        print("Alert window has successfully closed")
    except TimeoutException as err:
        print("No alert window has found", err)


# get id and password from environment variables
ID = os.environ["kyobobook_id"]
PASSWORD = os.environ["kyobobook_password"]
is_logged_in = False

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

driver.get("http://www.kyobobook.co.kr")
driver.implicitly_wait(10)

# main page -> login page
login_btn = driver.find_element(by=By.CSS_SELECTOR, value="#gnbLoginInfoList > li > a")
login_btn.click()
driver.implicitly_wait(10)
time.sleep(1)

# login page
id_box = driver.find_element(by=By.NAME, value="memid")
password_box = driver.find_element(by=By.NAME, value="pw")
submit_btn = driver.find_element(by=By.CSS_SELECTOR, value="input.btn_submit")

id_box.send_keys(ID)
password_box.send_keys(PASSWORD)
submit_btn.click()
driver.implicitly_wait(5)

# daily attendance check
attendance_btn = driver.find_element(by=By.CSS_SELECTOR, value="#gnbLoginInfoList > li:nth-child(3) > a")
attendance_btn.click()
driver.implicitly_wait(5)
handle_alert()

# bonus stamp by choosing randomly selected answer (50% of probability)
answer_css_path = "#choice? > span.cover > img"
random_choice = random.randint(1, 2)
answer_css_path = answer_css_path.replace("?", str(random_choice))

answer_elem = driver.find_element(by=By.CSS_SELECTOR, value=answer_css_path)
answer_elem.click()

submit_btn = driver.find_element(
    by=By.CSS_SELECTOR,
    value="#container > div.main_area > div:nth-child(3) > div > div.killingpart > a",
)
submit_btn.click()

driver.implicitly_wait(5)
handle_alert()

driver.execute_script("logout();")
driver.implicitly_wait(7)

print("successfully signed-out!")
time.sleep(2) # to see the result on the browser
driver.quit()
