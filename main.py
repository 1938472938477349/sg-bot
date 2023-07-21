import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from dotenv import load_dotenv
from termcolor import colored

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import logging
from datetime import datetime
import schedule


def sg_chrome(profile):
    options = webdriver.ChromeOptions()
    options.add_argument(os.environ.get("CHROME_USER_DATA"))
    options.add_argument(profile)
    options.add_argument('--no-sandbox')
    # options.add_argument('--window-size=800,600')
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # options.add_argument("disable-extensions")
    # options.add_argument("--start-maximized")
    # options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    driver = webdriver.Chrome(service=Service(os.environ.get("CHROME_DRIVER_PATH")), options=options)
    driver.get(os.environ.get("URL"))
    games = driver.find_elements(By.CLASS_NAME, "giveaway__heading__name")
    maximum_i = len(games)
    i = 0
    entered = []
    for i in range(0,maximum_i):
        time.sleep(2)
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
                driver.back()
        except:
            driver.back()
    driver.close()
    print(entered)

def sg_firefox(prof):
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.binary_location = os.environ.get("PATH_FIREFOX")
    options.profile = prof
    driver = webdriver.Firefox(service=Service(executable_path=os.environ.get("PATH_GECKODRIVER")),options=options)
    driver.get(os.environ.get("URL"))
    time.sleep(2)

    # check privacy pop-up
    logging.info("Checking privacy statement...")
    privacy = driver.find_elements(By.CLASS_NAME, "ncmp__btn")
    if (len(privacy) != 0):
        privacy[1].click()
        logging.info("Privacy accepted.")


    # get profile name
    name = driver.find_element(By.CLASS_NAME, "nav__avatar-outer-wrap")
    logging.info("Logged into: " + name.get_attribute("href"))

    # get profile points
    points = driver.find_element(By.CLASS_NAME, "nav__points")
    logging.info("Points: " + str(points.text))

    # entering
    logging.info("Starting...")
    games = driver.find_elements(By.CLASS_NAME, "giveaway__row-inner-wrap")
    maximum_i = len(games)
    i = 0
    for i in range(0, maximum_i):
        all_games = driver.find_elements(By.CLASS_NAME, "giveaway__row-inner-wrap")
        if ("is-faded" not in all_games[i].get_attribute('class')):
            title = all_games[i].find_element(By.CLASS_NAME, "giveaway__heading__name")
            title.click()
            try:
                if (len(driver.find_elements(By.CLASS_NAME, "sidebar__error")) != 0):
                    points = driver.find_element(By.CLASS_NAME, "nav__points")
                    logging.info("Leftover points: " + str(points.text))
                    logging.info("Exiting... ")
                    break
                else:
                    enter_button = driver.find_element(By.CLASS_NAME, "sidebar__entry-insert")
                    game_title = driver.find_element(By.CLASS_NAME, "featured__heading__medium")
                    logging.info("Entering: " + str(game_title.text))
                    enter_button.click()
                    driver.back()
                    time.sleep(1)
            except:
                driver.back()
                time.sleep(1)
    driver.close()



def check_sg():
    logging.info("Executing job on: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    profiles = ["meqq84jj.P1", "ciqu7n01.P2", "ahxyhu19.P3"]
    for profile in profiles:
        try:
            sg_firefox(os.environ.get("PATH_FIREFOX_PROFILES") + profile)
        except:
            logging.info("Something went wrong with " + profile)



if __name__ == '__main__':
    logging.basicConfig(filename='log.txt', encoding='utf-8', level=logging.INFO)
    load_dotenv()

    check_sg()

    schedule.every().hour.do(check_sg)
    logging.info("Starting scheduler on: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    while True:
        schedule.run_pending()
        time.sleep(1)
