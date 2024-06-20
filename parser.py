import os
from typing import Any
from urllib.parse import urljoin

import django
from django.core.management import call_command
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from parser_api.models import Product
from utilities import split_string, create_json_file, bulk_create_product


BASE_URL = "https://www.mcdonalds.com/"

FULL_MENU_URL = urljoin(BASE_URL, "ua/uk-ua/eat/fullmenu.html")


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Parser.settings")
django.setup()


class Parser:
    _driver: WebDriver | None = None

    _product_list = None

    def get_driver(self) -> WebDriver:
        return self._driver

    def set_driver(self, driver: WebDriver) -> None:
        self._driver = driver

    @staticmethod
    def get_detailed_url(soup: BeautifulSoup):
        ls = soup.select("div.product-category > ul.cmp-category__row .cmp-category__item-link")
        detailed_url = []
        for url in ls:
            detailed_url.append(url.get("href"))
        return detailed_url

    def parse_detailed_page(self, url) -> dict[str, Any]:
        detail_page = urljoin(BASE_URL, url)
        driver = self.get_driver()
        driver.get(detail_page)
        panel = driver.find_element(By.CLASS_NAME, "cmp-accordion")
        buttons = panel.find_elements(By.TAG_NAME, "button")
        buttons[0].click()
        product = {}

        product["title"] = driver.find_elements(
            By.CSS_SELECTOR,
            "span.cmp-product-details-main__heading-title"
        )[1].text

        product["description"] = driver.find_element(
            By.CSS_SELECTOR,
            "div.cmp-product-details-main__description"
        ).text

        # Collect all energy values
        energy_values = driver.find_elements(By.CSS_SELECTOR, '.value > [aria-hidden="true"].sr-only')
        for i, nutrition in enumerate(("calories", "fats", "carbs", "proteins")):
            product[nutrition] = energy_values[i].text
        # Collect all nutrients
        nutrients_value = driver.find_elements(
            By.CSS_SELECTOR,
            '.cmp-nutrition-summary__details-column-view-desktop > '
            'ul > .label-item > .value > .sr-only'
        )

        for i, nutrients in enumerate(("unsaturated_fats", "sugar", "salts", "portion")):
            if not nutrients_value:
                continue
            product[nutrients] = split_string(nutrients_value[i].text)
        print(product)
        return product

    def parser(self):
        page = requests.get(FULL_MENU_URL)
        soup_page = BeautifulSoup(page.content, "html.parser")
        all_urls = self.get_detailed_url(soup_page)
        product_list = []
        for url in all_urls:
            try:
                product_list.append(self.parse_detailed_page(url))
            except StaleElementReferenceException:
                product_list.append(self.parse_detailed_page(url))

        return product_list

    def main(self):
        with webdriver.Chrome() as driver:
            self.set_driver(driver)
            self._product_list = self.parser()
        create_json_file(self._product_list)
        bulk_create_product(self._product_list)


def run_parser():
    parser = Parser()
    parser.main()
