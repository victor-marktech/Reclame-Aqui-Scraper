from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

import csv
import os
import argparse

import constants


def arguments():
    parser = argparse.ArgumentParser('Reclame Aqui Scraper')
    parser.add_argument('-i', '--id', help='Link ou ID da empresa no Reclame Aqui',
                        action='store', dest='id', required=True)
    parser.add_argument('-p', '--pages', help='Número de páginas para coletar',
                        action='store', dest='pages', required=True, type=int)
    parser.add_argument('-f', '--file', help='Nome do arquivo em que será salvo os dados da coleta',
                        action='store', dest='file', required=True)
    parser.add_argument('-b', '--browser', help='Browser que será utilizado para a coleta, (F) para Firefox e (C) para Chrome',
                        action='store', dest='browser', nargs='?', default="f")
    args = parser.parse_args()
    return args


def driver_chrome():
    chrome_options = ChromeOptions()
    chrome_options.headless = True
    driver = webdriver.Chrome(options=chrome_options, executable_path=ChromeDriverManager(
    ).install(), service_log_path=None)
    return driver


def driver_firefox():
    firefox_options = FirefoxOptions()
    firefox_options.headless = True
    # Set the path to the geckodriver executable
    # geckodriver_path = os.path.join(os.path.dirname(__file__), 'bin', 'geckodriver')
    geckodriver_path = "/snap/bin/firefox.geckodriver"

    # Set up the Firefox driver with the geckodriver path
    service = Service(geckodriver_path)

    driver = webdriver.Firefox(options=firefox_options, service=service)
    return driver


def define_browser(argument):
    if (argument.lower() == "c" or argument.lower() == "chrome"):
        return driver_chrome()
    if (argument.lower() == "f" or argument.lower() == "firefox"):
        return driver_firefox()
    raise Exception("Invalid browser argument.")


def csv_writer(reclamacao, nome):
    with open('Arquivos/{}.csv'.format(nome),
              'a', encoding='utf8', newline='') as arquivo_csv:
        writer = csv.DictWriter(
            arquivo_csv, fieldnames=constants.CSV_FILE_HEADERS)
        file_is_empty = os.stat('Arquivos//{}.csv'.format(nome)).st_size == 0
        if file_is_empty:
            writer.writeheader()
        writer.writerow(reclamacao)


def format_url(url):
    url_str = str(url)
    return url_str.replace("(", "").replace(")", "").replace("'", "").replace(",", "")
