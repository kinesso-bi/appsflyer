from selenium import webdriver
from time import sleep
import os
from glob import glob
import json
import pandas as pd
from datetime import datetime, timedelta

cwd = os.getcwd()

with open("auth/client_secrets.json", "r") as jsonFile:
    data = json.load(jsonFile)

username = data["admin"]["client_id"]
password = data["admin"]["client_secret"]

url = 'https://hq1.appsflyer.com/auth/login'

"""get data last 90 days"""
for interval in range(1, 91):
    sleep(2)
    options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': cwd}
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(r"C:\\Users\\Tomasz.Pionka\\Downloads\\chromedriver.exe", options=options)
    print(url)
    driver.get(url)
    sleep(5)
    driver.find_element_by_name('username').send_keys(username)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_css_selector('.submit-btn').click()
    sleep(5)
    custom_date = (datetime.now() - timedelta(days=interval)).strftime("%Y-%m-%d")
    link = 'https://hq1.appsflyer.com/custom-dashboard#end={date_target}&grouping=attribution&pageId=89652&start={date_target}'.format(
        date_target=custom_date)
    driver.get(link)
    sleep(5)
    try:
        driver.find_element_by_css_selector(
            "body > div:nth-child(6) > div.fade.in.modal > div > div > div.confirmation-dialog-header.modal-header > button").click()
    except:
        pass
    sleep(5)
    i = 1
    while True:
        try:
            sleep(2)
            driver.find_element_by_xpath(
                """//*[@id="export-wrapper"]/div[2]/div[{}]/div/div/div[1]/div/div/button""".format(i)).click()
            print("dropdown click")
            sleep(2)
            driver.find_element_by_xpath(
                """//*[@id="export-wrapper"]/div[2]/div[{}]/div/div/div[1]/div/div/ul/li[4]""".format(i)).click()
            print("export click")
            i += 1
        except:
            break

    print('finish')
    driver.close()
    driver.quit()
    sleep(1)

    filenames = [
        'Android Per Ad.csv',
        'Android Per Adset.csv',
        'Android Per campaign.csv',
        'iOS Per Ad.csv',
        'iOS Per Adset.csv',
        'iOS Per campaign.csv'
    ]

    for filename in filenames:
        try:
            df = pd.read_csv(filename)
            if len(df.index) > 0:
                df['Date'] = custom_date
                df.to_csv("output/{}_{}.csv".format(filename.split(".")[0], custom_date), index=False)
                os.remove(filename)
            else:
                os.remove(filename)
        except:
            pass
