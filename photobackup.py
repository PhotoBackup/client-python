#!/usr/bin/env python3

"""PhotoBackup

Usage:
  photobackup.py upload <url> <image>
  photobackup.py test <url>
  photobackup.py (-h | --help)
  photobackup.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

# stdlib
import getpass
import hashlib
import sys
import urllib.parse
# pipped
from docopt import docopt
import requests
from blessings import Terminal
term = Terminal()


def password():
    """ Ask the password of the server. """
    password = getpass.getpass(prompt='The server password: ')
    return {'password': hashlib.sha512(password.encode('utf-8')).hexdigest()}


def response(status_code):
    if status_code == 200:
        print(term.green + "Request was successful!")
    elif status_code == 403:
        print(term.red + "ERROR: wrong password!")
    elif status_code == 404:
        print(term.red + "ERROR: unknown address!")
    elif status_code == 405:
        print(term.red + "ERROR: the server does not know this url!")
    elif status_code == 408:
        print(term.red + "ERROR: request took too long!")
    elif status_code == 413:
        print(term.red + "ERROR: file too large, modify your server config!")
    elif status_code == 500:
        print(term.red + "ERROR: server made a booboo!")
    else:
        print(term.red + "ERROR: request failed ({})!".format(status_code))


def upload(url, image):
    upfile = {'upfile': open(image, 'rb')}
    try:
        request = requests.post(url, files=upfile, data=password())
    except requests.exceptions.MissingSchema:
        sys.exit(term.red + "ERROR: invalid URL: {}".format(url))
    except requests.exceptions.ConnectionError:
        sys.exit(term.red + "ERROR: Connection refused")

    response(request.status_code)


def test(url):
    test_url = urllib.parse.urljoin(url, '/test')

    try:
        request = requests.post(test_url, data=password())
    except requests.exceptions.MissingSchema:
        sys.exit(term.red + "ERROR: invalid URL: {}".format(url))
    except requests.exceptions.ConnectionError:
        sys.exit(term.red + "ERROR: Connection refused")

    response(request.status_code)


def main(args):
    if args['upload']:
        upload(args['<url>'], args['<image>'])
    elif args['test']:
        test(args['<url>'])


if __name__ == '__main__':
    arguments = docopt(__doc__, version='PhotoBackup Python CLI client, v1.0')
    main(arguments)
