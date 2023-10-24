"""
Assign number of lines between target character
"""
import argparse
import subprocess


def parse_arguments():
    """Parse and return command line arguments."""
    parser = argparse.ArgumentParser(description='Run a Scrapy spider.')
    parser.add_argument('--files', nargs='+',
                        help='Files name of target character in data folder. If not provided, all files will be used.')
    parser.add_argument('--name', nargs='+', type=str, required=True,
                        help='Name of target character, you should only provide one character once.')

    args = parser.parse_args()

    return args


def main():
    """Main function to run the Scrapy spider with given arguments."""
    args = parse_arguments()




if __name__ == '__main__':
    main()
