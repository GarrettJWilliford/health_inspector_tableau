import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bsoup
import re
import json
import time

def driver_init_chrome(headless = True):
    if not headless:
        return webdriver.Chrome(executable_path = r'/Users/garrettwilliford/Downloads/chromedriver-2')
    fop = Options()
    fop.add_argument('--headless')
    fop.add_argument('--window_size1920x1080')
    return webdriver.Chrome(executable_path = r'/Users/garrettwilliford/Downloads/chromedriver-2', options = fop)

def driver_init():
    return webdriver.PhantomJS(executable_path = r'/Users/garrettwilliford/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs')


def hyperlink_append(final, link):
    data = pd.DataFrame()
    data['hyperlinks'] = [link]
    final = final.append(data)
    return final


def hyperlink_paste():
    final = pd.DataFrame()
    final['hyperlinks'] = []
    while True:
        link = input('>> ').strip()
        if a == 'EXIT':
            break
        final = hyperlink_append(final, link)
    return final
    

def extract_info(driver, link):
    driver.get(link)
    td = driver.find_elements_by_tag_name('td')
    inspector = [t.get_attribute('innerHTML') for t in td if 'bdrBR' in t.get_attribute('outerHTML') and 'Print:' in t.get_attribute('innerHTML')][1][28::]
    address = [re.sub('&nbsp;', '', t.get_attribute('innerHTML')[t.get_attribute('innerHTML').index('>') + 1::]).strip() for t in td if 'Physical Address:'\
               in t.get_attribute('innerHTML')][0]
    violations = [tt for tt in [re.sub('&nbsp;', '', t.get_attribute('innerHTML')) for t in td if 'center padL' in t.get_attribute('outerHTML')] if len(tt) != 0]    
    return violations, address, inspector



def dataframe_webscraper(data, driver = False):
    if not driver:
        driver = driver_init()
    final = {'Violations' : [], 'Address' : [], 'Inspector' : []}
    iteration = 1
    for d in data['LINK']:
        while True:
            try:
                violations, address, inspector = extract_info(driver, d)
                final['Violations'].append(violations)
                final['Address'].append(address)
                final['Inspector'].append(inspector)
                print('<<<<<<<<<<(' + str(iteration) + '/' + str(len(data)) + ')>>>>>>>>>>')
                print(inspector)
                print(address)
                print(violations)
                pickle.dump(final, open('df_merge_static.p', 'wb'))
                time.sleep()
                iteration += 1
                break
            except:
                print('<<!|DRIVER_FAILED|!>>')
    if not driver:
        driver.quit()      
    return pd.DataFrame(final)
        
         

def format_dataframe(data, scraped_data):
    data['NUMBER OF VIOLATIONS'] = data['Violations'].apply(lambda x: len(x))



def client_id():
    Client_ID = '8686c761d3182d6d8499bf7ef711556921f22a2b'
    return Client_ID

def api_key():
    api_key = "RtDiIsUaEE5iZJGscWuiVJ3x-Gi6aHkDIdfv44NZphf7kJa3R4G68dCYmO0nkmMi6OEqpmPbqPLLz7MLu20Xw39qTOtCDloyDFmD5XQuVaA42KVKsTRiYsUv-qMXXnYx"
    return api_key


def driver_check():
    driver = webdriver.PhantomJS(executable_path = r'/Users/garrettwilliford/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs')
    print('<>')
    driver.get('https://ww.bbc.com')
    print('<>')
    t = driver.find_elements_by_tag_name('media__link')
    for tt in t:
        print(tt.get_attribute('innerHTML'))

