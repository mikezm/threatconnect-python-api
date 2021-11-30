# Overview
-----------
This is an unofficial app built to facilitate API requests to the ThreatConnect platform. Developers looking to build 
Python apps for the ThreatConnect platform should consider using [TCEX](https://github.com/ThreatConnect-Inc/tcex) as
the officially supported framework. 

The following Python script is an example that can be used to test connectivity to ThreatConnect’s API
and simple requests. 

# Setting up the app
-------
1. In the `app` folder, rename the `config-template.py` file to `config.py`.
2. Update the following variables in the `config.py` file:
   - API_ID
   - API_SECRET
   - API_HOST _(without `/api` in the URL.)_
   - DEFAULT_OWNER

# Testing API connectivity
Execute `./tcapi.py --test` or `python3 tcapi.py --test`. 

If the script was executed successfully, all Organizations and Communities that the API credentials have access will be returned.

# How To Use the app

The `tcapi.py` app can test connectivity with the `--test` flag, but can also be used to other API requests

For the help instructions run `python3 tcapi.py -h`

- `-h, --help`: print the help details
- `--test`: tests connectivity to the ThreatConnect API
- `-u, --url`: set the URL for the API request
- `-m, --method`: set the METHOD for the API request (GET, POST, PUT, DELETE)
- `--data`: set the request body (e.g. POST data)
- `--data-binary`: provide a JSON file 
- `-o, --out-file`: set the output file (JSON response data will be written to a file instead of printed to screen)
- `-v, --verbose`: verbose output. Shows Signature, Headers, URL, and Status Code of Response

## Python Requirements
Requires the `requests` library. 

This can be installed with `pip3 install requests` or `pip3 install -r requirements.txt`.
