#!/usr/bin/python3

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
import os.path

from app.request import no_data_request, data_request
import argparse
import json
import sys
import os.path

DEFAULT_URL = "/api/v2/owners"

parser = argparse.ArgumentParser()
parser.add_argument("--test", dest="test_connectivity", action='store_true', help="Test API connectivity")
parser.add_argument("-u", "--url", dest="url",
                    help="endpoint URL. E.G. {}".format(DEFAULT_URL))
parser.add_argument("-m", "--method", dest="method", help="Request Method",
                    choices=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
parser.add_argument("-d", "--data", dest="data", help="JSON request body")
parser.add_argument("--data-binary", dest="data_file", help="Request Body file (JSON)")
parser.add_argument("-o", "--out-file", dest="out_file", help="Output file")
parser.add_argument("-v", "--verbose", dest="verbose", action='store_true', default=False, help="Verbose output")


def run():
    json_data = None

    args = parser.parse_args()

    if args.test_connectivity:
        args.url = DEFAULT_URL
        args.method = 'GET'

    # check for URL
    if not args.url:
        print("ERROR: URL required unless running with '--test' flag")
        parser.print_help()
        sys.exit(1)

    # check for method
    if not args.method:
        print("ERROR: Method required unless running with '--test' flag")
        parser.print_help()
        sys.exit(1)

    # clean up URL
    url = args.url
    if not args.url.startswith('/api'):
        url = "/api{}".format(args.url)

    # check for valid JSON
    if args.data:
        try:
            json_data = json.loads(args.data)
        except json.decoder.JSONDecodeError:
            print("ERROR: invalid JSON")
            sys.exit(1)

    # check if file exists
    if args.data_file:
        if not os.path.exists(args.data_file):
            print("ERROR: file not found -> '{}'".format(args.data_file))
            sys.exit(1)

        # check if file contains valid JSON
        with open(args.data_file, 'r') as f:
            try:
                json_data = json.load(f)
            except json.decoder.JSONDecodeError:
                print("ERROR: invalid JSON in file -> {}".format(args.data_file))
                sys.exit(1)

    # check for valid output file path
    if args.out_file:
        out_file_path = os.path.split(args.out_file)[0]
        if not os.path.exists(out_file_path):
            print("ERROR: Output file path invalid -> {}".format(out_file_path))
            sys.exit(1)

    if json_data:
        res = data_request(url, args.method, json_data, args.verbose)
    else:
        res = no_data_request(url, args.method, args.verbose)

    if args.verbose:
        print("----------------------------------")
        print("Response: ")
        print("status code: {}".format(res.status_code))

    # response data
    parsed = json.loads(res.text)
    response_data = json.dumps(parsed, indent=2)

    if args.out_file:
        with open(args.out_file, 'w') as out_file:
            out_file.write(response_data)
    else:
        print(response_data)


if __name__ == '__main__':
    run()
