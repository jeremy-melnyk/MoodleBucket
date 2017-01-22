import os

import requests
import mimetypes
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import unquote, quote

URL = 'https://my.concordia.ca/psp/upprpr9/?cmd=login&languageCd=ENG&'
TIMEOUT = 10
PARSER = 'html.parser'
DOWNLOAD_PATH = "downloads/"


def load_courses(credentials):
    browser = webdriver.PhantomJS()
    browser.get(URL)
    username_el = browser.find_element_by_id('userid')
    username_el.send_keys(credentials['netname'])
    password_el = browser.find_element_by_id('pwd')
    password_el.send_keys(credentials['password'])
    password_el.submit()
    try:
        wait = WebDriverWait(browser, TIMEOUT)
        wait.until(EC.element_to_be_clickable((By.ID,'layout-table')))
    except TimeoutException as ex:
        browser.close()
        print(str(ex))
        return
    try:
        soup = BeautifulSoup(browser.page_source, PARSER)
        course_table = soup.find('table', {'id': 'layout-table'})
        if course_table is None:
            return
        course_links = course_table.find_all('a')
        if course_links is None:
            return
        with requests.Session() as session:
            for link in course_links:
                response = session.get(link.get('href'))
                course_soup = BeautifulSoup(response.text, PARSER)
                documents = course_soup.find_all('div', {'class': 'activityinstance'})
                if documents is None:
                    continue
                header = course_soup.find('div', {'class': 'page-header-headings'})
                if header is None:
                    continue
                course_title = header.find('h1').text
                for document in documents:
                    item_link = document.find('a')
                    if item_link is None:
                        continue
                    document_response = session.get(item_link.get('href'))
                    content_type = document_response.headers['content-type']
                    extension = mimetypes.guess_extension(content_type)
                    if(extension == '.pdf'
                       or extension == '.docx'
                       or extension == '.doc'
                       or extension == '.pptx'
                       or extension == '.txt'):
                        subdirectory_name = course_title + '/'
                        directory_name = DOWNLOAD_PATH + subdirectory_name
                        if not os.path.exists(directory_name):
                            os.makedirs(directory_name)
                        clean_url = unquote(document_response.url.split('/')[-1])
                        file_name = clean_url
                        target_path = directory_name + file_name
                        download_file(document_response, target_path)
                        print("Downloading: " + file_name)
        print("Downloads complete.")
    except Exception as ex:
        print(str(ex))
    browser.close()


def download_file(response, target_path):
    handle = open(target_path, "wb")
    for chunk in response.iter_content(chunk_size=512):
        if chunk:  # filter out keep-alive new chunks
            handle.write(chunk)
