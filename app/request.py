# =============================================================================
# Copyright 2021 ThreatConnect, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

import requests
import hashlib
import hmac
import time
import base64
import json
from urllib.parse import quote_plus, unquote_plus
from app.config import *


def encode_url(uri):
    unquoted = unquote_plus(uri)
    return quote_plus(unquoted, safe='/=?')


def no_data_request(uri, method, verbose=False):
    url = encode_url(uri)
    request_headers = make_request_headers(url, method, verbose)
    return requests.request(method=method, url=API_HOST+url, headers=request_headers)


def data_request(uri, method, data, verbose=False):
    url = encode_url(uri)
    request_headers = make_request_headers(url, method, verbose)
    return requests.request(method=method, url=API_HOST+url, headers=request_headers, json=data)


def make_request_headers(path, method, verbose):
    ts = int(time.time())

    signature = "{0}:{1}:{2}".format(path, method, ts)

    hmac_signature = hmac.new(SECRET_KEY.encode(), signature.encode(), digestmod=hashlib.sha256).digest()
    encoded_signature = base64.b64encode(hmac_signature).decode()
    auth_header = "TC {0}:{1}".format(ACCESS_ID, encoded_signature)
    headers = {
        'Timestamp': str(ts),
        'Authorization': auth_header,
        'Content-Type': 'application/json; charset=utf-8'
    }
    if verbose:
        print('URL: {}'.format(path))
        print('Method: {}'.format(method))
        print('Signature: {}'.format(signature))
        print('Headers: ', json.dumps(headers, indent=2))

    return headers

