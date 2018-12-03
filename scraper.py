import argparse
import sys
import requests
import re


def create_parser():
    """ gets url from command line arguments """
    descripion = "Extracts URLs, email addresses," \
        + " and phone numbers from specified website"
    parser = argparse.ArgumentParser(description=descripion)
    parser.add_argument('url', help='url of website to be parsed')
    return parser


def main(url):
    r = requests.get(url)
    content = re.sub(r"<[^>]*>", " ", r.content)
    print_emails(content)
    print_urls(content)
    print_phone_numbers(content)


def print_emails(content):
    print("\nEmails")
    email_regex = re.compile(
        r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
    emails = email_regex.findall(content)
    for email in emails:
        print(email)


def print_phone_numbers(content):
    print("\nPhone Numbers")

    phone_regex = re.compile(
        r'1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]'
        + r'{2})\W*([0-9]{4})(\se?x?t?(\d*))?')
    phone_numbers = phone_regex.findall(content)
    for number in phone_numbers:
        print('{}-{}-{}'.format(number[0], number[1], number[2]))


def print_urls(content):
    print("\nURLs")
    url_regex = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]'
        + r'|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    urls = url_regex.findall(content)
    for url in urls:
        print(url)


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])
    main(args.url)
