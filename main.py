import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from dotenv import load_dotenv
from termcolor import colored


load_dotenv()

def sg(profile):
    options = webdriver.ChromeOptions()
    options.add_argument(os.environ.get("CHROME_USER_DATA"))
    options.add_argument(profile)
    # options.add_argument('--no-sandbox')
    options.add_argument('--window-size=800,600')
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(os.environ.get("CHROME_DRIVER_PATH")), options=options)
    driver.get(os.environ.get("URL"))
    games = driver.find_elements(By.CLASS_NAME, "giveaway__heading__name")
    maximum_i = len(games)
    i = 0
    entered = []
    for i in range(0,maximum_i):
        game = driver.find_elements(By.CLASS_NAME, "giveaway__heading__name")[i]
        title = game.text
        game.click()
        try:
            if (len(driver.find_elements(By.CLASS_NAME, "sidebar__error")) != 0):
                print(colored("POINT LIMIT REACHED", "red"))
                break
            else:
                enter_button = driver.find_element(By.CLASS_NAME, "sidebar__entry-insert")
                enter_button.click()
                entered.append(str(title))
                time.sleep(1)
                driver.back()
        except:
            driver.back()
    driver.close()
    print(entered)

profiles = ["profile-directory=Default", "profile-directory=Profile 1", "profile-directory=Profile 3"]
for profile in profiles:
    sg(profile)
