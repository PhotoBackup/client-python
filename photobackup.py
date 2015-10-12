#!/usr/bin/env python3
# Copyright (C) 2013-2015 Stéphane Péchard.
#
# This file is part of PhotoBackup.
#
# PhotoBackup is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PhotoBackup is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

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
import os
import sys
import urllib.parse
# pipped
from docopt import docopt
import requests
from blessings import Terminal
term = Terminal()


def make_data(filepath=None):
    """ Ask the password of the server. """
    password = getpass.getpass(prompt='The server password: ')
    data = {'password': hashlib.sha512(password.encode('utf-8')).hexdigest()}
    if filepath:
        data['filesize'] = os.stat(filepath).st_size
    return data


def response(status_code):
    if status_code == 200:
        print(term.green + "Request was successful!")
    elif status_code == 400:
        print(term.red + "ERROR: missing file size in request!")
    elif status_code == 403:
        print(term.red + "ERROR: wrong password!")
    elif status_code == 404:
        print(term.red + "ERROR: unknown address!")
    elif status_code == 405:
        print(term.red + "ERROR: the server does not know this url!")
    elif status_code == 408:
        print(term.red + "ERROR: request took too long!")
    elif status_code == 411:
        print(term.red + "ERROR: file sizes do not match!")
    elif status_code == 413:
        print(term.red + "ERROR: file too large, modify your server config!")
    elif status_code == 500:
        print(term.red + "ERROR: server made a booboo!")
    else:
        print(term.red + "ERROR: request failed ({})!".format(status_code))


def upload(url, image):
    upfile = {'upfile': open(image, 'rb')}
    try:
        request = requests.post(url, files=upfile, data=make_data(image))
    except requests.exceptions.MissingSchema:
        sys.exit(term.red + "ERROR: invalid URL: {}".format(url))
    except requests.exceptions.ConnectionError:
        sys.exit(term.red + "ERROR: Connection refused")

    response(request.status_code)


def test(url):
    test_url = urllib.parse.urljoin(url, '/test')

    try:
        request = requests.post(test_url, data=make_data())
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
    arguments = docopt(__doc__, version='PhotoBackup Python CLI client, v0.1.0')
    main(arguments)
