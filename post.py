#!/usr/bin/env python3.8
import sys
import os
import base64
from urllib.parse import urlencode, urljoin, urlparse
from urllib.request import Request, urlopen

def post():
    url="https://gruppe5.web7012.cweb04.gamingweb.de/"
    post_data = {
        "Benutzername": 'asdf',
        "Passwort": 'asdf'
    }
    post_body = urlencode(post_data).encode("utf-8")
    request = Request(url, data=post_body, method="POST")
    response = urlopen(request)
    print(response.status)
    print(response.read().decode("utf-8"))

post()