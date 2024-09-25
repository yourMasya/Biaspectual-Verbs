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

        with open('biaspectives_relevant_list.txt', 'r', encoding='utf-8') as file:
            words = file.read().split()

        for word in words:
            print(f"Processing word: {word}")
            perfective_data, imperfective_data, both_posssible = scrapper.process_word(word)

            with open(os.path.join(
                    output_dir, f'{word}_perf.json'), 'w', encoding='utf-8') as f:
                json.dump(perfective_data, f, ensure_ascii=False, indent=4)

            with open(os.path.join(
                    output_dir, f'{word}_imp.json'), 'w', encoding='utf-8') as f:
                json.dump(imperfective_data, f, ensure_ascii=False, indent=4)

            with open(os.path.join(
                    output_dir, f'{word}_both.json'), 'w', encoding='utf-8') as f:
                json.dump(both_posssible, f, ensure_ascii=False, indent=4)

    except FileNotFoundError as fnf_error:
        print(f"File not found error: {fnf_error}")
    except json.JSONDecodeError as json_error:
        print(f"JSON decode error: {json_error}")
    finally:
        if scrapper:
            scrapper.close()


if __name__ == "__main__":
    main()
