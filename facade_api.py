"""
FacadeAPI module to provide a high-level interface for web scraping operations.
"""

from typing import Optional, Any, Tuple, List, Dict
from pathlib import Path

from selenium.common import WebDriverException

from scrapper import Scrapper
from config.config_loader import load_config
from driver_init import init_driver

CONFIG_PATH = Path(__file__).parent.parent / 'scrapper_config.json'


class FacadeAPI:
    """
    FacadeAPI serves as a high-level interface to interact with the Scrapper class.
    """

    def __init__(self, config_path: Path = CONFIG_PATH):
        """
        Initialize the FacadeAPI with configurations and a Scrapper instance.

        Args:
            config_path (str): Path to the configuration JSON file.
        """
        self.config = load_config(config_path)
        self.driver = init_driver(self.config.get("headless", True))
        self.scrapper = Scrapper(self.driver, self.config)

    def process_word(self, word: str) -> (
            Optional)[Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]]:
        """
        Processes a given word using the Scrapper to collect relevant data.

        Args:
            word (str): The word to be processed and scraped.

        Returns:
            Optional[Dict[str, Any]]:
            Scraped data associated with the word, or None if an error occurs.
        """
        try:
            self.scrapper.navigate_to_search()
            self.scrapper.input_word(word)
            # self.scrapper.set_page_size()
            return self.scrapper.collect_data(word)
        except WebDriverException as e:
            print(f"Error processing word '{word}': {e}")
            return None

    def close(self):
        """
        Closes the WebDriver instance to clean up resources.
        """
        self.scrapper.close_driver()
