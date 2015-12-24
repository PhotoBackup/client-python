[![Python Version](https://img.shields.io/badge/Python-3-brightgreen.svg?style=plastic)](http://python.org) [![Code Issues](https://www.quantifiedcode.com/api/v1/project/8c46c0185dbf4d6097f2c92e08e67536/badge.svg)](https://www.quantifiedcode.com/app/project/8c46c0185dbf4d6097f2c92e08e67536)

# PhotoBackup Python client
A simple console Python 3 client for PhotoBackup. It is mostly used to test servers.
You can use it with:

    $ python photobackup.py upload http://myserver.com/ image.jpg

or test it with:

    $ python photobackup.py test http://myserver.com/

A password is asked to the user, then the request is operated.
When the request to the server is done, the response status is shown.
You got:

 * 200 when the request was successful ;
 * 400 when the request was badly formed ;
 * 403 when the given password is not the same as the server's one ;
 * 408 when the request timed out ;
 * 500 when an error occured on the server in the meanwhile.

See the [official API](https://github.com/PhotoBackup/api/blob/master/api.raml) for more information.

## Installation with the Makefile
You can use the included `Makefile` to build a virtual Python environment:

    make && source venv/bin/activate

If I were you, that's what I would do.


## Installation without virtual environment
You can use the client directly if you have all dependencies already available.
Those are:

* [`blessings`](https://pypi.python.org/pypi/blessings/) for a bit of color ;
* [`docopt`](http://docopt.org/) for an easy command-line interface ;
* [`requests`](http://docs.python-requests.org/) for easy HTTP requests.
