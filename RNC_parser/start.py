"""
Main script to start the web scraping process.
"""

import json
import os
from pathlib import Path

from facade_api import FacadeAPI


def main():
    """
    Main function to initiate the web scraping process for words listed
    in 'biaspectual_verbs.txt'.
    Scraped data for each word will be saved in separate JSON files
    in the 'biaspectual_verbs' directory.
    """
    scrapper = None
    output_dir = 'biaspectual_verbs'

    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        config_path = Path('config/scrapper_config.json')
        scrapper = FacadeAPI(config_path=config_path)

        with open('dict_articles_urls.json', 'r', encoding='utf-8') as file:
            articles_urls = json.load(file)
            words = articles_urls.keys()

        aspects = ["perf", "impf"]
        for word in words:
            print(f"Processing word: {word}")
            for aspect in aspects:
                print(f"Current aspect: {aspect}")
                occurrences = scrapper.process_word(word, aspect=aspect)
                if occurrences:
                    with open(os.path.join(
                            output_dir, f'{word}_{aspect}.json'), 'w', encoding='utf-8') as f:
                        json.dump(occurrences, f, ensure_ascii=False, indent=4)

    except FileNotFoundError as fnf_error:
        print(f"File not found error: {fnf_error}")
    except json.JSONDecodeError as json_error:
        print(f"JSON decode error: {json_error}")
    finally:
        if scrapper:
            scrapper.close()


if __name__ == "__main__":
    main()
