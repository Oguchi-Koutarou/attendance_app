from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep
import logging
from datetime import datetime
import os

os.environ['DISPLAY'] = ':0.0'

# ログの設定
logging.basicConfig(filename='app_webopen.log', 
                    level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def web_open(url, debug):
    try:
        driver_service = Service('/usr/bin/chromedriver')
        if debug == 1:
            driver = webdriver.Chrome(service=driver_service)   
        else:    
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(service=driver_service, options=options)
        
        driver.implicitly_wait(120)    
        driver.get(url)
        logging.info("Web Opened!")
        sleep(60) # ページがしっかり読み込まれるまで待機してサーバーを起こす
        driver.quit()
    except Exception as e:
        logging.exception(f"Error occurred! : {e}")

def main(debug):
    # ご自身のアンケートアプリのURLに変更
    url_1 = "https://27nov-tmu-reunion-questionnaire.streamlit.app/"
    url_list = [url_1]

    for url in url_list:
        web_open(url, debug)

if __name__ == '__main__':
    debug = 0
    main(debug)
