import json
from typing import Dict, List

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Browser:
    """Represents a browser instance."""

    def __init__(self) -> None:
        """Initializes the browser."""
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )

    def get(self, url: str) -> None:
        """Navigates to the specified URL."""
        self.driver.get(url)

    def find_element(self, by: By, selector: str) -> WebElement:
        """Finds elements on the page."""
        return self.driver.find_element(by, selector)

    def find_elements(self, by: By, selector: str) -> List[WebElement]:
        """Finds elements on the page."""
        return self.driver.find_elements(by, selector)

    def quit(self) -> None:
        """Closes the browser."""
        self.driver.quit()


class PageExtractor:
    """Extracts verbs and their corresponding article URLs from a Wiktionary category page."""

    def __init__(self, browser: Browser, base_url: str) -> None:
        """
        Initializes the PageExtractor.

        Args:
            browser: The browser instance to use for navigation and element finding.
            base_url: The URL of the Wiktionary category page to extract from.
        """
        self.browser = browser
        self.base_url = base_url
        self.wait = WebDriverWait(self.browser.driver, 15) # Adjust timeout as needed
        self.verb_dict_articles: Dict[str, str] = {}

    def _extract_verbs_from_page(self) -> Dict[str, str]:
        """Extracts verbs and their URLs from the current page."""
        page_dict_articles = {}
        entries = self.browser.find_elements(By.CSS_SELECTOR, '#mw-pages > div')
        for entry in entries:
            verb_elements = entry.find_elements(By.TAG_NAME, 'a')
            for verb_element in verb_elements:
                article_url = verb_element.get_attribute('href').strip()
                verb = verb_element.text.strip()
                if verb and verb != 'рещи':
                    page_dict_articles[verb] = article_url
        return page_dict_articles

    def extract_biaspectives(self) -> None:
        """Extracts verbs and their URLs from the Wiktionary category page."""
        self.browser.get(self.base_url)
        page_counter = 1
        try:
            while page_counter < 8:
                print(f'Processing page: {page_counter}')
                self.wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'div.mw-category-generated')
                    )
                )

                self.verb_dict_articles.update(self._extract_verbs_from_page())

                next_page_button = self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            f'#mw-pages > a:nth-child({3 if page_counter == 1 else 4})'
                        )
                    )
                )
                next_page_button.click()
                page_counter += 1
        except TimeoutException:
            pass
        finally:
            self.browser.quit()
            print('Extraction finished')

    def save_results(self, filename: str = 'dict_articles_urls.json') -> None:
        """Saves the extracted verb-to-article URL's mapping to a JSON file."""
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(
                self.verb_dict_articles,
                file,
                ensure_ascii=False,
                indent=4
            )


class MorphonologyExtractor:
    """Extracts morphemes and stress of biaspectual verbs by pair verb-URL given."""
    def __init__(self, browser: Browser, path2urls: str) -> None:
        """
        Initializes the PageExtractor.

        Args:
            browser: The browser instance to use for navigation and element finding.
            path2urls: path to .json file with biaspectual verbs and URLs referencing to their Wicktionary page
        """
        self.browser = browser
        self.path2urls = path2urls
        self.morphonology_dataset = []
        self.wait = WebDriverWait(self.browser.driver, 3)

    def _extract_verb_morphonology(self, verb: str, url: str) -> Dict[str, str]:
        """Extracts verb morphonology by pair verb-URLs from the current page."""
        verb_morphonology = {}
        self.browser.get(url)
        verb_features = self.browser.find_elements(By.TAG_NAME, 'p')
        stress = verb_features[0].text.strip()
        morphemes = verb_features[2].text.strip()
        if '[Тихонов, 1996]' in morphemes:
            verb_morphonology['лемма'] = verb if verb else ''
            verb_morphonology['ударение'] = stress if stress else ''
            verb_morphonology['морфемный разбор'] = morphemes if morphemes else ''
            return verb_morphonology

    def _load_articles_dict(self) -> Dict[str, str]:
        with open(self.path2urls, 'r', encoding='utf-8') as file:
            dict_articles_urls = json.load(file)
            return dict_articles_urls

    def parse_morphonology_dataset(self) -> None:
        try:
            dict_articles_urls = self._load_articles_dict()
            for verb, url in dict_articles_urls.items():
                morphonology_item = self._extract_verb_morphonology(verb, url)
                if morphonology_item:
                    self.morphonology_dataset.append(morphonology_item)
        except IndexError as e:
            print(e)
        finally:
            self.browser.quit()
            print('Dataset created')
        # обработай ошибку, если всё полетит и датасет не создастя

    def save_results(self, filename: str) -> None:
        """Saves the extracted morphonology dictionary as a JSON file."""
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(
                self.morphonology_dataset,
                file,
                ensure_ascii=False,
                indent=4
            )


if __name__ == "__main__":
    base_url = 'https://ru.wiktionary.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%94%D0%B2%D1%83%D0%B2%D0%B8%D0%B4%D0%BE%D0%B2%D1%8B%D0%B5_%D0%B3%D0%BB%D0%B0%D0%B3%D0%BE%D0%BB%D1%8B'
    browser = Browser()
    page_extractor = PageExtractor(browser, base_url)
    page_extractor.extract_biaspectives()
    page_extractor.save_results('dict_articles_urls.json')
    morphonology_extractor = MorphonologyExtractor(browser, 'dict_articles_urls.json')
    morphonology_extractor.parse_morphonology_dataset()
    morphonology_extractor.save_results('morphonology_dataset.json')
    with open('biaspectives_relevant_list.txt', 'w', encoding='utf-8') as f:
        for word in morphonology_extractor.morphonology_dataset:
            print(word['лемма'], file=f)

