from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def login():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.implicitly_wait(15)

    # driver.get('https://app.procore.com/365280/project/drawing_areas')
    driver.get('https://app.procore.com/365280/project/prime_contracts/1501578/payment_applications/949374/owner_billing')

    email_element = driver.find_element_by_css_selector("#session_email")
    email_element.send_keys("tbabatsikos@modernniagara.com")

    password_element = driver.find_element_by_css_selector("#session_password")
    password_element.send_keys("Modern@TB1")

    wait = WebDriverWait(driver, 10) # will repeatedly search for element until it is clickable, max search time is 10 sec
    login_button = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[@id='login-btn']")))
    login_button.click()

    # time.sleep(0.2) ################################ MANUAL WAIT #####################################
    return driver


def get_rows(driver):
    rows = []
    while(True):
        try:
            # table = driver.find_element_by_css_selector(".Style_taflan-body__1mej-")
            # rows = table.find_elements_by_xpath("./tbody/tr")
            rows = driver.find_elements_by_xpath("//tr")
            if(len(rows) > 0):
                # for row in rows:
                    # asd = row.get_attribute('class')
                break
        except Exception as e:
            print("bricked getting rows: [%s]" % e)
            pass
    print("num rows: %s" % len(rows))
    return rows

# def select_all_dropdowns(driver):
#     print("done waiting for page load...")
    
#     rows = get_rows(driver)

#     checkpoint = 0
#     yuh = 0
#     for row in rows:
#         if(checkpoint != 2):
#             try:
#                 if(row.get_attribute('class') == "Style_taflan-group-row__3PGhk Style_tier-1__3AMWO"):
#                     checkpoint += 1
#             except Exception as e:
#                 pass
#         else:
#             try:
#                 selector = row.find_element_by_xpath("./td/select")
#                 selector.click()
#                 time.sleep(0.3)
#                 dropdown_option = row.find_element_by_xpath("./td/select/option[@value='31206']")
#                 dropdown_option.click()
#                 print("clicked dropdown...")
#                 time.sleep(7)
#                 print("done waiting, getting rows...")
#                 # rows = get_rows(driver)
#                 checkpoint = 0
#             except Exception as e:
#                 print("bricked trynna get dropdown_option [%s]" % e)
#                 pass

def select_dropdown(driver):
    rows = get_rows(driver)

    checkpoint = 0
    yuh = 0
    for row in rows:
        if(checkpoint != 2):
            try:
                if(row.get_attribute('class') == "Style_taflan-group-row__3PGhk Style_tier-1__3AMWO"):
                    checkpoint += 1
            except Exception as e:
                break
        else:
            try:
                selector = row.find_element_by_xpath("./td/select")
                selector.click()
                time.sleep(0.3)
                dropdown_option = row.find_element_by_xpath("./td/select/option[@value='31206']")
                dropdown_option.click()
                print("clicked dropdown, sleepin...")
                # time.sleep(2)
                checkpoint = 0
            except Exception as e:
                print("bricked trynna get dropdown_option [%s]" % e)
                pass
    return -1

# driver = login()
# select_all_dropdowns(driver)

ctr = 0
while(True):
    driver = login()
    print("got new driver...")
    select_dropdown(driver)
    driver.quit()
    print("quit driver...")
    if(ctr == 850):
        break
    ctr += 1

time.sleep(3)