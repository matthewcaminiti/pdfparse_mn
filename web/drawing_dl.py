from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def get_selected_drawing(drawing_name="mp2-094", with_markup=False):
	driver = webdriver.Chrome(ChromeDriverManager().install())
	driver.implicitly_wait(15)

	driver.get('https://app.procore.com/365280/project/drawing_areas')

	email_element = driver.find_element_by_css_selector("#session_email")
	email_element.send_keys("tbabatsikos@modernniagara.com")

	password_element = driver.find_element_by_css_selector("#session_password")
	password_element.send_keys("Modern@TB1")

	wait = WebDriverWait(driver, 10) # will repeatedly search for element until it is clickable, max search time is 10 sec
	login_button = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[@id='login-btn']")))
	login_button.click()

	time.sleep(0.2) ################################ MANUAL WAIT #####################################

	# ifcs = driver.find_element_by_xpath("//a[@href='/365280/project/drawing_areas/331943/drawing_log/list']")
	ifcs = wait.until(ec.element_to_be_clickable((By.XPATH, "//a[@href='/365280/project/drawing_areas/331943/drawing_log/list']")))
	ifcs.click()

	drawing_search = driver.find_element_by_css_selector(".input__src-SearchBar__35akm.searchOverrides_input__obJ_8")
	drawing_search.send_keys(drawing_name + '\n')

	rows = []
	while(True):
		try:
			rows = driver.find_elements_by_css_selector(".tableRow__src-Table__1GzYi.tableOverrides_tableRow__2RCv8")
			if(len(rows) > 0):
				break
		except Exception as e:
			pass

	time.sleep(0.5) ################################ MANUAL WAIT #####################################

	drawing_nums = driver.find_elements_by_css_selector(".fullscreen-drawing-viewer.DrawingLog_table-display-cell__EoZHE")
	for nums in drawing_nums:
		if(nums.text.lower() == drawing_name.lower()):

			spec_row = nums.find_element_by_xpath("../..")
			drawing_num_cell = spec_row.find_elements_by_xpath("./div")[0]
			radio_button = drawing_num_cell.find_element_by_xpath("./label")
			while(True):
				try:
					radio_button.click()
					break
				except Exception as e:
					pass
				

			while(True):
				try:
					baits = driver.find_elements_by_xpath("//span[@class='ellipsis']")
					if(len(baits) > 0):
						for bait in baits:
							if(bait.text.lower().strip() == "Download Drawings".lower().strip()):
								bait.click()
								break
						break
				except Exception as e:
					pass
	
	if(with_markup):
		wait = WebDriverWait(driver, 10) # will repeatedly search for element until it is clickable, max search time is 10 sec
		while(True):
			try:
				# baits = driver.find_elements_by_xpath("//input[@class='_10bpE-6_8_1']")
				baits = driver.find_elements_by_css_selector("._10bpE-6_8_1")
				if(len(baits) > 0):
					for bait in baits:
						if("with markup" in bait.text.lower()):
							with_markup_radio = bait.find_element_by_xpath("./../input[@class='_2kgRY-6_8_1']")
							# with_markup_radio = wait.until(ec.element_to_be_clickable(bait.find_element_by_xpath("./../input[@class='_2kgRY-6_8_1']")))
							with_markup_radio.click()
							break
					break
			except Exception as e:
				pass

	time.sleep(0.5) ################################ MANUAL WAIT #####################################

	dl_button = driver.find_element_by_css_selector("._3tTvo-6_8_1.bPEPj-6_8_1._1nJNI-6_8_1")
	dl_button.click()

	time.sleep(5) ################################ MANUAL WAIT #####################################
