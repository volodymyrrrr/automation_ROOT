encoding="utf-8"
import csv
import os
import time
import gspread
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import Service
from fake_useragent import UserAgent

ua = UserAgent

client = gspread.service_account('Tests/gs_credentials.json')
working_sheet = client.open_by_url(
    'https://docs.google.com/spreadsheets/d/1fRi9qAdb-E-xAY_jQiMdjjEsN1xZZdxK6865V-Ck6RE/edit#gid=0')
wb1 = working_sheet.get_worksheet(1)
URLS = wb1.get_values('B2:H500')
if os.path.exists("links2.csv"):
    os.remove("links2.csv")
else:
    print("The file does not exist")

with open("links2.csv", "w", newline='') as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(("links", "tangiblee", "number", "Root_ID", "popup_selector", "Skip", "useragent"))
for urls in URLS:
    with open("links2.csv", 'a', newline='') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(
            urls
        )


def test_cicle(driver, ):
    with open("links2.csv", "r", newline='') as file1:
        reader = csv.DictReader(file1, delimiter=";")
        for line in reader:
            cta = line["tangiblee"]
            url = line["links"]
            r = line["number"]
            ID = line["Root_ID"]
            popup = line["popup_selector"]
            skip = line["Skip"]
            useragent = line["useragent"]
            if skip == 'TRUE':
                print('scip')
            else:
                driver_service = Service()
                options = webdriver.ChromeOptions()
                options.add_argument("--incognito")
                options.add_argument(useragent)
                options.add_argument("--headless")
                driver = webdriver.Chrome(service=driver_service, options=options)
                driver.maximize_window()
                driver.delete_all_cookies()
                try:
                    driver.get(url)
                    time.sleep(5)
                    try:
                        driver.find_element(By.ID, ID).shadow_root.find_element(By.CSS_SELECTOR, popup).click()
                        time.sleep(5)
                        driver.execute_script("scrollBy(0,550);")
                        try:
                            Wait(driver, timeout=5).until(EC.presence_of_element_located((By.CLASS_NAME, cta)))
                            wb1.update_cell(row=r, col=9, value="Pass")
                        except:
                            wb1.update_cell(row=r, col=9, value="false")
                    except:
                        wb1.update_cell(row=r, col=9, value="Popup_error")
                except:
                    wb1.update_cell(row=r, col=9, value="Load_error")
    driver.close()
