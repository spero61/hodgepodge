import os, time, re, sys, random

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
    UnexpectedAlertPresentException,
)

# automation processes of Quasarzone point mining
def main():
    login()  # 사이트 로그인 (10pt)
    main_banner()  #  메인 페이지 대형 사이드 배너(10pt)
    attendance_check()  # 오전 9시 이후 출석체크 (10-30pt)
    hot_deal_ads()  # 지름/할인정보 우측하단 배너(0-3pt)
    build_pc_ads()  # PC조립/견적 배너(10pt)
    logout()


# login page
def login():
    driver.get("https://quasarzone.com/login?nextUrl=https://quasarzone.com/")

    id_box = driver.find_element(by=By.NAME, value="login_id")
    password_box = driver.find_element(by=By.NAME, value="password")
    login_btn = driver.find_element(by=By.CSS_SELECTOR, value="div.top-input-area p a")

    id_box.send_keys(ID)
    password_box.send_keys(PASSWORD)
    login_btn.click()
    driver.implicitly_wait(3)

    # to check whether a user has successfully signed-in
    handle_alert(is_login=True)

    # get prev_point as an "Int" obj
    global prev_point
    prev_point = get_point()
    print("prev_point:\t", prev_point)


# daily attendance check
def attendance_check():
    driver.get("https://quasarzone.com/users/attendance/")
    driver.execute_script("anttendanceCheck();")
    handle_alert()


# main banner ads (10pt each)
# need to figure out why automatic alert close does not work properly sometimes
def main_banner():
    driver.get("https://quasarzone.com/bbs/qn_partner")
    ads_clicked = []
    count = 1
    for _ in range(random.randint(10, 25)):
        try:
            # page refresh to get another main banner advertisement
            driver.refresh()
            driver.implicitly_wait(3)
            main_ad = driver.find_element(
                by=By.CSS_SELECTOR,
                value="#container > aside.logo-area.left > section > ul > li > a",
            )
            onclick_text = main_ad.get_attribute("onclick")
            tmp = re.findall("[0-9]", onclick_text)
            hashed_link = "".join(tmp)

            if hashed_link in ads_clicked:
                print(f"Same ad has detected. Skipping...: {count}")
                count += 1
                continue
            ads_clicked.append(hashed_link)
            print("Found main ad!")

        except NoSuchElementException:
            print("Google AdSence has found, skip this page")
            continue

        try:
            main_ad.click()
            driver.implicitly_wait(7)
            driver.switch_to.window("main_tab")
            handle_alert()
            time.sleep(0.5)

        except UnexpectedAlertPresentException:
            print("Ahhhhhh!! please close the alert manually")
            driver.implicitly_wait(3)
            time.sleep(1)


# hot deals ads (0 to 3 pt each)
def hot_deal_ads():
    driver.get("https://quasarzone.com/bbs/qb_saleinfo/")
    ad_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="ul.banner-multi-wrap > li > a"
    )

    for elem in ad_elements:
        elem.click()
        driver.implicitly_wait(12)
        driver.switch_to.window("main_tab")
        handle_alert()
        time.sleep(0.5)


# build your PC page - sponsor ads (10pt each)
def build_pc_ads():
    driver.get("https://quasarzone.com/bbs/qf_hwjoin")
    sponsor_elems = driver.find_elements(by=By.CSS_SELECTOR, value=".sponsor-logo > a")
    for elem in sponsor_elems:
        elem.click()
        driver.implicitly_wait(7)
        driver.switch_to.window("main_tab")
        handle_alert()
        time.sleep(0.5)


# calculate points earned during this session then perform sign-out
def logout():
    # go to the main page
    driver.get("https://quasarzone.com")
    driver.implicitly_wait(3)

    # check if a user has signed-in
    try:
        logout_btn = driver.find_element(by=By.CLASS_NAME, value="logout-bt")
    except NoSuchElementException:
        print("You have not signed-in yet")
        sys.exit(3)

    # calculate points earned during the session
    global prev_point
    current_point = get_point()
    print("current_point:\t", current_point)
    print(f"You earned {current_point - prev_point} pt!😁")

    # perform sign-out
    logout_btn.click()
    driver.implicitly_wait(3)
    time.sleep(1)


# handle alert window to accept
def handle_alert(is_login=False):
    try:
        WebDriverWait(driver, 3).until(
            expected_conditions.alert_is_present(),
            "Timed out waiting for simple alert to appear",
        )
        alert = driver.switch_to.alert
        alert.accept()
        if is_login:
            print("Please check id and password!")
            sys.exit(1)
        else:
            print("Alert window has successfully closed")
    except TimeoutException as err:
        print("No alert window has found", err)


# return Quasarzone point as an Int
def get_point():
    try:
        point_raw = driver.find_element(
            by=By.CSS_SELECTOR,
            value="#content > div > div.top-content-area > div.right-util-wrap > div.login-action-wrap > div.user-info-wrap > div > p > a:nth-child(2) > span",
        ).text
        point_raw = re.findall("[0-9]", point_raw)
        point = int("".join(point_raw))
        return point
    except NoSuchElementException:
        print("Could not get point containing element")
        sys.exit(2)


if __name__ == "__main__":
    # get id and password from environment variables
    ID = os.environ["quasarzone_id"]
    PASSWORD = os.environ["quasarzone_password"]

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

    driver.get("https://quasarzone.com/")
    driver.implicitly_wait(3)
    driver.maximize_window()

    main()

    driver.quit()
