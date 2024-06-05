#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 16:44:20 2024

@author: adi
"""

import requests
from bs4 import BeautifulSoup
import mysql.connector
from collections import Counter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
from urllib.parse import urlparse
from duckduckgo_search import DDGS
import pandas as pd
from PyPDF2 import PdfReader
from io import BytesIO



engines = ['Google','Yahoo', 'Bing','DuckDuckGo']
#engines = ['DuckDuckGo']
chromedriver_path = "C:/Users/msari/Downloads/chromedriver.exe"
service = Service(executable_path=chromedriver_path)

def google_search(query):
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.google.com/")
    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Let the page load
    
    # Initialize a dictionary to store unique base URLs
    unique_base_urls = {}
    titles = []
    
    search_results = driver.find_elements(By.CSS_SELECTOR, 'h3.LC20lb.MBeuO.DKV0Md')
    

    for result in search_results:
        href = result.find_element(By.XPATH, './ancestor::a').get_attribute('href')
        parsed_url = urlparse(href)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        title_text = result.text
        # Check if the URL is not from google.com and is not already in unique_base_urls dictionary
        if 'www.google.com' not in base_url and base_url not in unique_base_urls and title_text != '':
            unique_base_urls[base_url] = True
            titles.append(title_text)
            

    driver.quit()
    return list(unique_base_urls.keys()), titles

def yahoo_search(query):
    driver = webdriver.Chrome(service=service)
    driver.get("https://search.yahoo.com/")
    try:
        search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "p")))
    except TimeoutException: # type: ignore
        print("Timeout occurred while waiting for the search box to load.")
        driver.quit()
        return []

    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2) 
    
    unique_base_urls = {}
    titles = []
    
    urls = driver.find_elements(By.CSS_SELECTOR, 'h3.title a')
    for i in range(0, len(urls)):
        href = urls[i].get_attribute('href')
        parsed_url = urlparse(href)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        title_text = urls[i].get_attribute('aria-label')
        
        # Check if the URL is not already in unique_base_urls dictionary
        if 'yahoo.com' not in base_url and base_url not in unique_base_urls and title_text is not None:
            titles.append(title_text)
            unique_base_urls[base_url] = True

    driver.quit()
    return list(unique_base_urls.keys()), titles

def bing_search(query):
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.bing.com/")
    try:
        search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
    except TimeoutException: # type: ignore
        print("Timeout occurred while waiting for the search box to load.")
        driver.quit()
        return []

    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  
    
    unique_base_urls = {}
    titles = []
    
    urls = driver.find_elements(By.CSS_SELECTOR, 'h2 a')
    for a in urls:
        href = a.get_attribute('href')
        parsed_url = urlparse(href)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        title_text = a.text
        if 'bing.com' not in base_url and base_url not in unique_base_urls and title_text != '':
            unique_base_urls[base_url] = True
            titles.append(title_text)

    driver.quit()
    return list(unique_base_urls.keys()), titles






# MySQL connection parameters
mySQLparams = {
    'host': 'localhost',
    'user': 'root',
    'database': 'MY_CUSTOM_BOT',
    'password': '1234'
}


add_search = 'INSERT INTO searches(query,engine) values(%s, %s)'
add_search_results = 'INSERT IGNORE INTO search_results_v2(url,search_id,title) values(%s,%s,%s)'


def populate_database(input_query, engine):
    if engine == 'Google':
        url_list, titles = google_search(input_query)
    elif engine == 'Yahoo':
        url_list, titles = yahoo_search(input_query)
    elif engine=="Bing":
        url_list, titles = bing_search(input_query)
    else:
        url_list, titles = duckduckgo_search(input_query)

        
    connection = mysql.connector.connect(**mySQLparams)
    cursor = connection.cursor()
    

    cursor.execute(add_search, (input_query, engine))
    search_id = cursor.lastrowid


    for i in range(0, len(url_list)):
        cursor.execute(add_search_results, (url_list[i], search_id, titles[i]))  


    connection.commit()
    cursor.close()
    connection.close()

def duckduckgo_search(query):
    results = DDGS().text(
        keywords=query,
        max_results=100
       )
    
    results_df = pd.DataFrame(results)
    return results_df['href'].tolist()[:100], results_df['title'].tolist()[:100]


def count_word_frequency(text, target_words):
    words = text.lower().split()
    word_count = Counter(words)
    word_frequency = {word: word_count[word] for word in target_words}
    return word_frequency


def frequencies(query):

    connection = mysql.connector.connect(**mySQLparams)
    cursor = connection.cursor()
    
    cursor.execute("SELECT url, url_id FROM search_results_v2")
    urls = cursor.fetchall()
    
    target_words = query.split(" ")
    
    url_word_frequency = {}
    proxies = [
    'http://proxy1.example.com:port',
    'http://proxy2.example.com:port',
    
    ]

    

    for url in urls:
        url_id = url[1]
        url = url[0]
        try:
            if ".pdf" in url:
                response = requests.get(url)
                if response.status_code == 200:
                    pdf_content = response.content
                    pdf_text = ""
                    pdf_reader = PdfReader(BytesIO(pdf_content))
                    for page in pdf_reader.pages:
                        pdf_text += page.extract_text()
                
                    frequency = count_word_frequency(pdf_text, target_words)
                    url_word_frequency[url_id] = frequency
                else:
                    print(f"Failed to fetch URL: {url}. Status code: {response.status_code}")
            
            else:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                           }
                proxy = {'http': proxies[0]}
                response = requests.get(url, headers=headers, proxies=proxy)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    text = soup.get_text()
                    text = text.replace("method", "methods")
                    frequency = count_word_frequency(text, target_words)
                    url_word_frequency[url_id] = frequency
                else:
                    print(f"Failed to fetch URL: {url}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch URL {url}: {e}")
        except Exception as e:
            print(f"Error processing URL {url}: {e}")

    
    for url_id, frequency in url_word_frequency.items():
        childhood_count = frequency['childhood']
        cancer_count = frequency['cancer']
        early_count = frequency['early']
        diagnosis_count = frequency['diagnosis']
        methods_count = frequency['methods']
        
        sql = "INSERT INTO URL_frequency (url_id, childhood_count, cancer_count, early_count, diagnosis_count, methods_count) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (url_id, childhood_count, cancer_count, early_count, diagnosis_count, methods_count)
        
        cursor.execute(sql, values)
    
    connection.commit()
    connection.close()
    
    
        

def automate_etl_process(search_term):
    for engine in engines:
        populate_database(search_term, engine)
    



if __name__ == '__main__':
    search_term = "childhood cancer early diagnosis methods"
    automate_etl_process(search_term)
    frequencies(search_term)
    
    
    
    