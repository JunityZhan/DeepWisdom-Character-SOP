import json
from langdetect import detect
import re


def load_config(file_path):
    """
    Load a JSON configuration file.

    Args:
    - file_path (str): Path to the configuration file.

    Returns:
    - dict: The loaded configuration.
    """
    with open(file_path, 'r') as file:
        return json.load(file)


config = load_config('spider.json')


class GeneralPipeline:
    """
    General pipeline for processing items.
    """

    def process_item(self, item, spider):
        """
        Remove extra whitespace from the text.

        Args:
        - item (dict): The item to be processed.
        - spider: The spider that generated the item.

        Returns:
        - dict: The processed item.
        """
        lines = [re.sub(r'\s+', ' ', line.strip()) for line in item['text'].split('\n') if line.strip()]
        item['text'] = '\n'.join(lines)
        return item


def get_language(text):
    try:
        return detect(text)
    except:
        return None


def get_text_length(text):
    language = get_language(text)
    if language == 'en':  # For English
        return len(text.split())
    elif language in ['zh', 'ja']:  # For Chinese and Japanese
        return len(text)
    else:
        return len(text.split())  # Default to word count


class ConfiguredPipeline:
    """
    Pipeline that processes items based on a configuration.
    """

    def should_remove_line(self, line, path_config):
        """
        Determine if a line should be removed based on the given configuration.

        Args:
        - line (str): The line to check.
        - path_config (dict): The configuration for the current URL path.

        Returns:
        - bool: True if the line should be removed, False otherwise.
        """
        line_length = get_text_length(line)

        if any(keyword in line for keyword in path_config.get('rm_line_keywords', [])):
            return True

        if line_length < path_config.get('min_line_len', 0):
            return True

        if line_length > path_config.get('max_line_len', float('inf')):
            return True

        return False

    def substitute_keywords(self, line, path_config):
        """
        Substitute keywords in a line based on the given configuration.

        Args:
        - line (str): The line to modify.
        - path_config (dict): The configuration for the current URL path.

        Returns:
        - str: The modified line.
        """
        for keyword, replacement in path_config.get('sub_keywords', {}).items():
            if keyword in line:
                line = line.replace(keyword, replacement)
        return line

    def process_item(self, item, spider):
        """
        Process an item based on the configuration.

        Args:
        - item (dict): The item to be processed.
        - spider: The spider that generated the item.

        Returns:
        - dict or None: The processed item or None if it should be discarded.
        """
        text = item['text'].split('\n')
        url_paths = item['url'].split('/')

        processed_text = []
        for line in text:
            should_append = True

            for path in url_paths:
                path_config = config.get(path, {})
                if any(keyword in line for keyword in path_config.get('rm_page_keywords', [])):
                    return None

                if self.should_remove_line(line, path_config):
                    should_append = False
                    break

                line = self.substitute_keywords(line, path_config)

            if should_append and line.strip():  # Check if line is not empty
                processed_text.append(line)

        item['text'] = '\n'.join(processed_text)
        return item
