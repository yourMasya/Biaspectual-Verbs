"""
Module for initializing a Selenium WebDriver instance.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def init_driver(headless: bool = True) -> webdriver.Chrome:
    """
    Initializes and returns a Selenium WebDriver instance for Chrome.

    Args:
        headless (bool): Determines whether to run the browser in headless mode.

    Returns:
        webdriver.Chrome: An instance of Chrome WebDriver with the specified options.
    """
    options = Options()

    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")

    return webdriver.Chrome(options=options)
