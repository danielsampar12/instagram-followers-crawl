import os
import csv
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


DRIVER_WAIT_TIME = 5

def startChrome(user_agent,executable_path):
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--incognito")
	chrome_options.add_argument("--headless")
	chrome_options.add_argument('--user-agent={}'.format(user_agent))
	chrome = webdriver.Chrome(options=chrome_options, executable_path=executable_path)
	return chrome


def waitForClass(driver, class_name, wait=None):
	if wait != None:
		element = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
	else:
		element = WebDriverWait(driver, DRIVER_WAIT_TIME).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
	return element


def waitForXpath(driver, xpath, wait=None):
	if wait != None:
		element = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.XPATH, xpath)))
	else:
		element = WebDriverWait(driver, DRIVER_WAIT_TIME).until(EC.presence_of_element_located((By.XPATH, xpath)))
	return element


def javaClick(driver, element):
	driver.execute_script("arguments[0].click();", element)



def randomSleep(min,max):
	random_wait = random.randint(min,max)
	time.sleep(random_wait)
	return random_wait


def createDirectory(folder):
	path = os.getcwd() + os.sep + folder
	if not os.path.exists(path):
		# os.mkdir(path)
		os.makedirs(path, exist_ok=True)
	return path


def writeCSV(filename, data_array):
	with open(filename + ".csv", 'a', encoding='utf-8-sig') as data:
		wr = csv.writer(data, quoting=csv.QUOTE_ALL, lineterminator='\r')
		wr.writerow(data_array)


