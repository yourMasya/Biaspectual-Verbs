"""
Parser module for web elements using Selenium.
"""

from typing import Optional, Dict
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class Parser:
    """
    A class used to parse web elements on a page using Selenium.
    """

    def __init__(self, driver: WebDriver, config: Dict):
        """
        Initializes the Parser with a WebDriver and configuration.

        Args:
            driver (WebDriver): The WebDriver instance to use.
            config (Dict): A dictionary containing configuration parameters.
        """
        self.driver = driver
        self.config = config
        self.wait = WebDriverWait(driver, config["timeout"])

    def extract_context(self, position: int) -> Optional[str]:
        """
        Extracts the context text of a web element located by a specific position.

        Args:
            position (int): The position of the web element to extract context from.

        Returns:
            Optional[str]: The extracted context text or None if extraction fails.
        """
        context_xpath = (
            f"(//span[@class='hit word'])[position()={position}]"
            "/ancestor::p[contains(@class, 'seq-with-actions')]"
        )
        try:
            return self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, context_xpath))).text.strip()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error extracting context: {e}")
            return None

    def extract_main_analysis(self) -> Optional[str]:
        """
        Extracts the method of homonymy resolution from the current page.

        Returns:
            Optional[str]: The extracted way of homonymy resolution: automatic or manual.
        """
        try:
            return self.wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, self.config["css_selectors"]["main_analysis"]))).text.strip()
            # print(el.is_displayed())
            # print(el.is_enabled())
            # print(el.text)
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error extracting main analysis: {e}")
            return None

    def extract_lemma(self) -> Optional[str]:
        """
        Extracts the lemma text from the current page.

        Returns:
            Optional[str]: The extracted lemma text or None if extraction fails.
        """
        try:
            return self.wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, self.config["css_selectors"]["lemma"]))).text.strip().lower()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error extracting lemma: {e}")
            return None

    def extract_grammar(self) -> Optional[str]:
        """
        Extracts the grammar information from the current page.

        Returns:
            Optional[str]: The extracted grammar information or None if extraction fails.
        """
        try:
            return self.wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, self.config["css_selectors"]["grammar"]))).text.strip()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error extracting grammar: {e}")
            return None

    def extract_semantics(self) -> Optional[str]:
        """
        Extracts semantics from the current page.

        Returns:
            Optional[str]: The extracted semantics text or None if extraction fails.
        """
        try:
            return self.wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, self.config["css_selectors"]["semantics"]))).text.strip()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error extracting semantics: {e}")
            return None

    def extract_related_words(self) -> Optional[str]:
        """
        Extracts related words from the current page.

        Returns:
            Optional[str]: The extracted related words text or None if extraction fails.
        """
        try:
            return self.wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, self.config["css_selectors"]["related_words"]))).text.strip()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error extracting related words: {e}")
            return None

    def extract_syntactic_properties(self) -> Optional[str]:
        """
        Iteratively tries to extract syntactic properties using different CSS selectors.

        Returns:
            Optional[str]: The extracted syntactic properties text or None if all attempts fail.
        """
        for css in self.config["css_selectors"]["syntactic_properties"]:
            try:
                text_present = EC.presence_of_element_located((By.CSS_SELECTOR, css))
                return self.wait.until(text_present).text.strip()
            except (NoSuchElementException, TimeoutException):
                continue
        return None

    def extract_additional_features(self) -> Optional[str]:
        """
        Iteratively tries to extract additional features using different CSS selectors.
        Returns:
            Optional[str]: The additional features words or None if extraction fails.
        """
        for css in self.config["css_selectors"]["additional_features"]:
            try:
                element_present = EC.presence_of_element_located((By.CSS_SELECTOR, css))
                return self.wait.until(element_present).text.strip()
            except (NoSuchElementException, TimeoutException):
                continue
        return None
