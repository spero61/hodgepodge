import os, random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
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

# to suppress error message of [32600:43916:0517/101436.565:ERROR:device_event_log_impl.cc(214)] [10:14:36.565] USB: usb_service_win.cc:415 Could not read device interface GUIDs
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# service = ChromeService(executable_path=CHROMEDRIVER_PATH)
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# open a new tab named 'main_tab' then switch to it
driver.execute_script("window.open('about:blank','main_tab');")
driver.switch_to.window("main_tab")

driver.get("http://www.kyobobook.co.kr")
driver.implicitly_wait(3)
driver.maximize_window()


# login page
driver.get(
    "http://www.kyobobook.co.kr/login/login.laf?Kc=GNHHNOlogin&orderClick=c03&retURL=http%3A//www.kyobobook.co.kr/index.laf"
)
driver.implicitly_wait(3)

id_box = driver.find_element(by=By.NAME, value="memid")
password_box = driver.find_element(by=By.NAME, value="pw")
login_btn = driver.find_element(by=By.CLASS_NAME, value="btn_submit")

id_box.send_keys(ID)
password_box.send_keys(PASSWORD)
login_btn.click()
driver.implicitly_wait(3)

# daily attendance check
driver.get("http://www.kyobobook.co.kr/event/dailyCheckSpci.laf?orderClick=c1j")
driver.implicitly_wait(3)
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

driver.implicitly_wait(3)
handle_alert()

driver.execute_script("logout();")
driver.implicitly_wait(3)

print("successfully signed-out!")
driver.quit()
